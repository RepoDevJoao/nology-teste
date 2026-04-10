# Nology Teste – Estagiário de Dev

Desafio técnico para a vaga de Estagiário de Desenvolvimento na Nology.

---

## Decisão de Negócio

> **Existe ambiguidade na regra de negócio. Optei por dobrar o valor final do cashback (após bônus VIP), pois a comunicação da promoção sugere benefício total ao cliente. Porém, em um cenário real, eu validaria essa regra com produto/comercial antes de implementar.**

---

## Estrutura do Projeto

```
nology-teste/
├── backend/         # API Python (FastAPI)
│   ├── main.py
│   ├── cashback.py
│   ├── database.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/        # Frontend estático (Vue CDN)
│   ├── index.html
│   └── Dockerfile
├── railway.toml
└── README.md
```

---

## Regras de Negócio

1. Cashback base: **5%** sobre o valor final da compra (após desconto)
2. Cliente VIP: **+10% adicional** sobre o cashback base
3. Compras acima de **R$ 500**: cashback **dobrado** (aplicado ao total após bônus VIP)

**Ordem de cálculo:**
```
valor_final = valor_bruto - desconto
cashback_base = valor_final * 0.05
cashback_vip = cashback_base * 0.10  (se VIP)
cashback_total = (cashback_base + cashback_vip) * 2  (se valor_final > 500)
```

---

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/calcular` | Calcula o cashback e salva a consulta no banco |
| `GET` | `/historico` | Retorna o histórico de consultas do IP solicitante |
| `GET` | `/health` | Healthcheck da API |

Para verificar o rastreio por IP diretamente no banco, acesse:
```
https://back-end-production-6ef7.up.railway.app/historico
```
Cada IP vê apenas suas próprias consultas. O retorno é um JSON com o IP identificado e a lista de consultas realizadas.

---

## Como rodar localmente

### Backend

```bash
cd backend
pip install -r requirements.txt
# Configure a variável DATABASE_URL com sua string de conexão PostgreSQL
uvicorn main:app --reload
```

### Frontend

Abra `frontend/index.html` diretamente no navegador, ou sirva com qualquer servidor estático.

---

## Deploy (Railway)

O projeto está configurado para deploy no Railway com dois serviços:
- **backend** – API FastAPI com PostgreSQL
- **frontend** – Servidor estático Nginx

Configure a variável de ambiente `DATABASE_URL` no serviço de backend com a URL do PostgreSQL provisionado pelo Railway.