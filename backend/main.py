# main.py
# API FastAPI – Calculadora de Cashback Nology

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from cashback import calcular_cashback
from database import init_db, salvar_consulta, buscar_historico_por_ip

app = FastAPI(title="Nology Cashback API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


# ── Schemas

class CashbackRequest(BaseModel):
    tipo_cliente: str = Field(..., description="'vip' ou 'comum'")
    valor_compra: float = Field(..., gt=0, description="Valor bruto da compra em R$")
    percentual_desconto: float = Field(0, ge=0, lt=100, description="Desconto em % (0 se não houver)")


class ConsultaHistorico(BaseModel):
    tipo_cliente: str
    valor_compra: float
    cashback: float
    criado_em: str


# ── Endpoints

@app.post("/calcular")
async def calcular(payload: CashbackRequest, request: Request):
    """Calcula o cashback e persiste a consulta no banco."""
    is_vip = payload.tipo_cliente.strip().lower() == "vip"

    resultado = calcular_cashback(
        valor_bruto=payload.valor_compra,
        percentual_desconto=payload.percentual_desconto,
        is_vip=is_vip,
    )

    # Captura IP real mesmo atrás de proxy (Railway usa X-Forwarded-For)
    ip = request.headers.get("x-forwarded-for", request.client.host)
    ip = ip.split(",")[0].strip()

    salvar_consulta(
        ip=ip,
        tipo_cliente=payload.tipo_cliente.strip().lower(),
        valor_compra=payload.valor_compra,
        cashback=resultado["cashback_final"],
    )

    return resultado


@app.get("/historico")
async def historico(request: Request):
    """Retorna o histórico de consultas do IP solicitante."""
    ip = request.headers.get("x-forwarded-for", request.client.host)
    ip = ip.split(",")[0].strip()

    rows = buscar_historico_por_ip(ip)

    return {
        "ip": ip,
        "consultas": [
            {
                "tipo_cliente": row["tipo_cliente"],
                "valor_compra": float(row["valor_compra"]),
                "cashback": float(row["cashback"]),
                "criado_em": row["criado_em"].isoformat(),
            }
            for row in rows
        ],
    }


@app.get("/health")
def health():
    return {"status": "ok"}