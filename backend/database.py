# database.py
# Gerenciamento da conexão PostgreSQL e criação do schema

import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    """Cria a tabela de consultas se não existir."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS consultas (
                    id SERIAL PRIMARY KEY,
                    ip VARCHAR(45) NOT NULL,
                    tipo_cliente VARCHAR(10) NOT NULL,
                    valor_compra NUMERIC(10, 2) NOT NULL,
                    cashback NUMERIC(10, 2) NOT NULL,
                    criado_em TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()


def salvar_consulta(ip: str, tipo_cliente: str, valor_compra: float, cashback: float):
    """Persiste uma consulta no banco."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO consultas (ip, tipo_cliente, valor_compra, cashback)
                VALUES (%s, %s, %s, %s)
                """,
                (ip, tipo_cliente, valor_compra, cashback),
            )
        conn.commit()


def buscar_historico_por_ip(ip: str) -> list:
    """Retorna o histórico de consultas de um IP específico."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tipo_cliente, valor_compra, cashback, criado_em
                FROM consultas
                WHERE ip = %s
                ORDER BY criado_em DESC
                """,
                (ip,),
            )
            return cur.fetchall()