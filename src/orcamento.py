from db import fetch, execute
import datetime

def definir_orcamento():
    mes = input("Mês (Ano-Mês): ")
    valor = float(input("Orçamento (€): "))

    existente = fetch("SELECT id FROM orcamento WHERE mes=%s", (mes,))

    if existente:
        execute("UPDATE orcamento SET valor=%s WHERE mes=%s", (valor, mes))
        print("Orçamento atualizado")
    else:
        execute("INSERT INTO orcamento (mes, valor) VALUES (%s , %s)", (mes, valor))
        print("Orçamento definido com sucesso!")

def ver_orcamento():
    mes_atual = datetime.datetime.now().strftime("%Y-%m")

    orcamento = fetch("SELECT valor FROM orcamento WHERE mes=%s", (mes_atual,))
    
    if not orcamento:
        print("Nenhum orçamento definido para este mês")
        return
    
    orcamento_valor = orcamento[0][0]

    total = fetch( """
        SELECT SUM(valor) FROM despesas
        WHERE DATE_FORMAT(data, '%Y-%m') = %s
    """, (mes_atual,))[0][0] or 0
    total = float(total)

    restante = orcamento_valor - total

    print(f"\n Mês: {mes_atual}")
    print(f"\n Orçamento: {orcamento_valor:.2f}")
    print(f"\n Gastos: {total:.2f}")
    print(f"\n Restante {restante:.2f}")

    if restante < 0:
        print("Ultrapassaste o orçamento!!!")


