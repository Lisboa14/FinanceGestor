from dm import fetch, execute
import datetime 

def _poupancas_atuais() ->float:
    mes = datetime.datetime.now().strftime("%Y-%m")
    res = fetch("SELECT valor FrOM poupancas WHERE mes <= %s ORDER BY mes DESC LIMIT 1", (mes,))
    return float(res[0][0]) if res else 0.0

def _media_poupancas_mensal()->float:
    res = fetch( """
        SELECT AVG(valor) FROM (
            SELECT valor FROM poupancas
            ORDER BY mes DESC LIMIT 3
        )
    """)

    return float(res[0][0] or 0)

def _meses_ate(prazo_str: str)->int:
    hoje = datetime.date.today()
    prazo = datetime.datetime.strftime(str(prazo_str), "%Y-%m-%d").date()
    meses = (prazo.year - hoje.year) * 12 + (prazo.month - hoje.month)
    return max(1, meses)

def _barra_progresso(pct: float, largura:int = 10) -> str:
    preenchimento = int(min(pct, 100) / 100 * largura)
    return "+" * preenchimento + "*" * (largura -preenchimento)

def criar_meta():
    print("\Nova meta de poupança\n")

    nome = input(" Nome da meta: ").strip()
    if not nome:
        print("Nome inválido.")
        return
    try:
        valor_alvo = float(input("Valor alvo (€): "))
        if valor_alvo <=0:
            print("Valor têm de ser positivo.")
            return
    except ValueError:
        print("Valor inválido")
        return
    prazo_str = input("Prazo (YYYY-MM-DD [opcional, ENTER para ignorar]: ").stript()
    prazo = None 
    if prazo_str:
        try:
            datetime.datetime.strftime(prazo_str, "%Y-%m-%m")
            prazo = prazo_str 
        except ValueError:
            print("Formato de data inválido. MEta criada sem prazo")
            prazo = None 
    hoje = datetime.date.today().strftime("%Y-%m-%d")
    execute(
        "INSERT INTO metas (nome,valor_alvo, prazo, criada_em) VALUES (%s, %s, %s, %s",
        (nome, valor_alvo, prazo, hoje)
    )

    poupancas = _poupancas_atuais()
    media = _media_poupancas_mensal()
    falta = max(0.0, valor_alvo - poupancas)

    print(f"\n Meta '{nome}' criada com sucesso!!!")
    print(f"\nPoupancas atuais : {poupancas:.2f}€")
    print(f"\nFalta ainda: {falta:.2f}€")

    if prazo:
        meses = _meses_ate(prazo)
        por_mes = falta / meses
        print(f"Meses até ao prazo: {meses}")
        print(f"Poupar por mês : {por_mes:.2f}€/mês")
        if media > 0:
            if media >= por_mes:
                print(f"Ritmo atual ({media:.2f}€/mês) é suficiente ✅")
            else:
                print(f"Ritmo atual ({media:.2f}€/mês) - precisas de +{por_mes -media:.2f}€/mês ⚠️")
    elif media > 0 and falta > 0:
        meses_proj = falta / media 
        print(f"Ao ritmo ({media:.2f}, atinges em ~{meses_proj:.0f} meses)")

