from db import fetch
from decimal import Decimal 
import datetime


def poupancas():
    mes_atual = datetime.datetime.now().strftime("%Y-%m")
    sql = """
        SELECT COALESCE(SUM(saldo), 0)
        FROM (
            SELECT
                o.mes,
                o.valor - COALESCE(SUM(d.valor), 0) AS saldo
            FROM orcamento o
            LEFT JOIN despesas d
                ON DATE_FORMAT(d.data, '%Y-%m') = o.mes
            WHERE o.mes < %s
            GROUP BY o.mes, o.valor
        ) AS saldos_mensais
    """

    resultado = fetch(sql, (mes_atual,))
    total = resultado[0][0] if resultado else 0

    return Decimal(str(total))    
