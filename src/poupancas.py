from db import fetch, execute

def poupancas(mes, orcamento, despesas):

    sql = """
    SELECT valor FROM poupancas
    WHERE mes < %s 
    ORDER BY mes DESC 
    LIMIT 1 
    """
    resultado = fetch(sql, (mes ,))

    poupancas_anteriores = resultado[0][0] if resultado else 0

    saldo = orcamento - despesas
    novas_poupancas = poupancas_anteriores + saldo

    sql_insert = """
    INSERT INTO poupancas (mes, valor)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE valor = %s 
    """    

    execute(sql_insert, (mes, novas_poupancas,novas_poupancas))

    return novas_poupancas
    
