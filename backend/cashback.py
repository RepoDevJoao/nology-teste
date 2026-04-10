# cashback.py
# Lógica de cálculo de cashback do programa Nology Fintech
#
# Regras (por ordem de aplicação):
#   1. Cashback base: 5% sobre valor final (após desconto)
#   2. Bônus VIP: +10% sobre o cashback base (apenas clientes VIP)
#   3. Promoção dobro: se valor_final > R$500, dobra o cashback total
#
# Decisão sobre ambiguidade:
#   O Documento 2 diz "o dobro de cashback" sem especificar se dobra apenas
#   o base ou o total com bônus VIP. Eu optei por dobrar o valor final do cashback
#   (após bônus VIP), pois a comunicação da promoção sugere benefício total ao
#   cliente. Em um cenário real, validaria essa regra com produto/comercial.


def calcular_cashback(valor_bruto: float, percentual_desconto: float, is_vip: bool) -> dict:
    """
    Calcula o cashback de uma compra.

    Args:
        valor_bruto: Valor original da compra em R$
        percentual_desconto: Percentual de desconto (ex: 20 para 20%)
        is_vip: True se o cliente é VIP

    Returns:
        dict com breakdown completo do cálculo
    """
    # Passo 1: valor final após desconto
    desconto = valor_bruto * (percentual_desconto / 100)
    valor_final = valor_bruto - desconto

    # Passo 2: cashback base (5% sobre valor final)
    cashback_base = valor_final * 0.05

    # Passo 3: bônus VIP (10% sobre cashback base)
    cashback_bonus_vip = cashback_base * 0.10 if is_vip else 0.0
    cashback_apos_vip = cashback_base + cashback_bonus_vip

    # Passo 4: promoção dobro (se valor_final > R$500)
    promocao_dobro_aplicada = valor_final > 500
    cashback_final = cashback_apos_vip * 2 if promocao_dobro_aplicada else cashback_apos_vip

    return {
        "valor_bruto": round(valor_bruto, 2),
        "percentual_desconto": percentual_desconto,
        "desconto_aplicado": round(desconto, 2),
        "valor_final": round(valor_final, 2),
        "cashback_base": round(cashback_base, 2),
        "cashback_bonus_vip": round(cashback_bonus_vip, 2),
        "cashback_apos_vip": round(cashback_apos_vip, 2),
        "promocao_dobro_aplicada": promocao_dobro_aplicada,
        "cashback_final": round(cashback_final, 2),
        "is_vip": is_vip,
    }