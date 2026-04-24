from db import fetch, execute
import datetime
import re 


def _validar_mes(mes: str) -> bool:
    if not re.match(r"^\d{4}-\d{2}$", mes):
        print("❌ Formato inválido. Usa YYYY-MM (ex: 2025-04)")
        return False
    ano, m = int(mes[:4]), int(mes[5:])
    if not (1 <= m <= 12):
        print("❌ Mês inválido. Deve ser entre 01 e 12.")
        return False
    if ano < 2000 or ano > 2100:
        print("❌ Ano inválido.")
        return False
    return True

def _validar_valor(valor_str: str) -> float | None:
    try:
        valor = float(valor_str.replace(",", "."))
    except ValueError:
        print("❌ Valor inválido. Usa um número (ex: 1200.00)")
        return None
    if valor <= 0:
        print("❌ O orçamento tem de ser maior que 0€.")
        return None
    if valor > 999999:
        print("❌ Valor demasiado alto.")
        return None
    return valor

def definir_orcamento():
    while True:
        mes = input("Mês (YYYY-MM): ").strip()
        if not _validar_mes(mes):
            continue

        mes_atual = datetime.datetime.now().strftime("%Y-%m")
        if mes < mes_atual:
            print("❌ Não podes definir orçamento para um mês que já passou.")
            continue
        break

    while True:
        valor_str = input("Orçamento (€): ").strip()
        valor = _validar_valor(valor_str)
        if valor is not None:
            break

    existente = fetch("SELECT id FROM orcamento WHERE mes=%s", (mes,))
    if existente:
        print("❌ Já existe um orçamento definido para este mês.")
        return

    execute("INSERT INTO orcamento (mes, valor) VALUES (%s, %s)", (mes, valor))
    print("Orçamento definido com sucesso!")

def ver_orcamento():
    orcamentos = fetch("SELECT mes, valor FROM orcamento ORDER BY mes DESC")

    if not orcamentos:
        print("Nenhum orçamento definido.")
        return

    mes_atual = datetime.datetime.now().strftime("%Y-%m")

    print(f"  {'Mês':<12} {'Orçamento':>12} {'Gasto':>10} {'Restante':>10} {'%':>7}  Estado")
    print("  " + "─" * 62)

    for mes, orcamento_valor in orcamentos:
        orcamento_valor = float(orcamento_valor)

        total = fetch("""
            SELECT SUM(valor) FROM despesas
            WHERE DATE_FORMAT(data, '%Y-%m') = %s
        """, (mes,))[0][0] or 0
        total    = float(total)
        restante = orcamento_valor - total
        pct      = (total / orcamento_valor * 100) if orcamento_valor > 0 else 0

        if restante < 0:
            estado = "Ultrapassado"
        elif pct >= 90:
            estado = "Quase no limite"
        elif mes == mes_atual:
            estado = "Em curso"
        elif mes > mes_atual:
            estado = "Ainda não chegou"
        else:
            estado = "Cumprido"

        marcador = "→ " if mes == mes_atual else "  "
        print(f"  {marcador}{mes:<10} {orcamento_valor:>12.2f}€ {total:>9.2f}€ {restante:>9.2f}€ {pct:>6.1f}%  {estado}")

    print("  " + "─" * 62)

def orcamento_dashboard():
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
    
    return restante 
