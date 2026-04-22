from db import fetch, execute
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
        ) sub 
    """)

    return float(res[0][0] or 0)

def _meses_ate(prazo_str: str)->int:
    hoje = datetime.date.today()
    prazo = datetime.datetime.strptime(prazo_str, "%Y-%m-%d").date()
    meses = (prazo.year - hoje.year) * 12 + (prazo.month - hoje.month)
    return max(1, meses)

def _barra_progresso(pct: float, largura:int = 10) -> str:
    preenchimento = int(min(pct, 100) / 100 * largura)
    return "+" * preenchimento + "*" * (largura -preenchimento)

def criar_meta():
    print("\nNova meta de poupança\n")

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
    prazo_str = input("Prazo (YYYY-MM-DD [opcional, ENTER para ignorar]: ").strip()
    prazo = None 
    if prazo_str:
        try:
            datetime.datetime.strptime(prazo_str, "%Y-%m-%d")
            prazo = prazo_str 
        except ValueError:
            print("Formato de data inválido. MEta criada sem prazo")
            prazo = None 
    hoje = datetime.date.today().strftime("%Y-%m-%d")
    execute(
        "INSERT INTO metas (nome,valor_alvo, prazo, criada_em) VALUES (%s, %s, %s, %s)",
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

def ver_metas():
    metas = fetch("SELECT id, nome, valor_alvo, prazo, criada_em, concluida FROM metas ORDER BY concluida, prazo")
    if not metas:
        print("\nAinda não tens metas definidas")
        return 
    poupancas =_poupancas_atuais()
    media= _media_poupancas_mensal()
    hoje = datetime.date.today()

    ativas = [m for m in metas if not m[5]]
    concluidas = [m for m in metas if m[5]]
    
    if ativas:
        print("\nMetas ativas\n")
        for meta in ativas:
            _mostrar_meta(meta, poupancas, media, hoje)

    if concluidas:
        print("\nMetas Concluídas\n")
        for meta in concluidas:
            id_,nome, valor_alvo, prazo, criada_em, _ = meta
            print(f"{nome} - {float(valor_alvo):.2f}€ (concluída)")

    _verificar_concluidas(poupancas)

def _mostrar_meta(meta, poupancas: float, media:float, hoje:datetime.date):
    id_,nome,valor_alvo, prazo, criada_em, _= meta 
    valor_alvo = float(valor_alvo)
    falta = max(0.0, valor_alvo - poupancas)
    pct = min(poupancas / valor_alvo * 100, 100) if valor_alvo > 0 else 0
    barra = _barra_progresso(pct)

    print(f"[{id_}]{nome}")
    print(f"{barra} {poupancas:.0f}€ / {valor_alvo:.0f}€ ({pct:.0f}%)")

    if prazo:
        prazo_dt = datetime.datetime.strftime(str(prazo), "%Y-%m,-%d").date()
        dias_restantes = (prazo_dt - hoje).days 
        meses_rest = _meses_ate(str(prazo))

        if dias_restantes <0:
            print(f"Prazo:{prazo} ⚠️ Prazo ultrapassado há {abs(dias_restantes)} dias")
        elif dias_restantes == 0:
            print(f"Prazo : HOJE")
        else :
            print(f"Prazo: {prazo} ({dias_restantes} dias restantes)")

        if falta > 0 and meses_rest >0:
            por_mes = falta / meses_rest
            if media >0:
                if media >=por_mes:
                    meses_proj = falta / media
                    print(f"Projeção:atinges em ~{meses_proj:.0f} meses ✅ (precisas {por_mes:.2f}€/mês")
                else:
                    print(f"⚠️ Risco:precisas {por_mes:.2f}€/mês, poupas {media:.2f}€/mês (+{por_mes -media:.2f}€ em falta)")
            else:
                print(f"Precisas de poupar {por_mes:.2f}€/mês para chegar a tempo")
        elif falta == 0:
            print(f"✅ Meta atingida!!! Pronta para concluir.")
    else:
        if falta > 0 and media > 0:
            meses_proj = falta / media
            print(f"Faltam {falta:.2f}€ ao ritmo atual atinges em ~{meses_proj:.0f} meses")
        elif falta ==0:
            print("✅ Meta atingida!!!")

def concluir_meta():
    meta = fetch("SELECT id, nome FROM metas WHERE concluida = 0")
    if not metas:
        print("\nSem metas ativas.")
        return
    
    print("\nMetas ativas:\n")
    for m in metas:
        print(f" [{m[0]}] {m[1]} - {float(m[2]):.2f}€")
    
    try:
        id_meta = int(input("\nID da meta a concluir"))
    except ValueError:
        print("ID inválido.")
        return 
    hoje = datetime.date.today().strftime("%Y-%m-%d")
    execute(
        "UPDATE metas SET conluida=1, conluida_em=%s WHERE id=%s",
        (hoje, id_meta)
    )
    meta = fetch("SELECT name FROM metas WHERE id=%s", (id_meta))
    nome = meta[0][0] if meta else "Meta"
    print(f"\n 🏆 Parabéns!!! Meta '{nome}' concluida!!!")

def _verificar_concluidas(poupancas: float):
    metas = fetch("SELECT id, nome, valor_alvo FROM metas WHERE concluida = 0")
    hoje = datetime.date.today().strftime("%Y-%m-%d")
    for id_,nome,valor_alvo in metas:
        if poupancas >= float(valor_alvo):
            execute(
                "UPDATE metas SET concluida=1, concluida_em=%s WHERE id%s",
                (hoje,id_)
            )
            print(f"\n 🏆 Meta atingida automaticamente: '{nome}' - {float(valor_alvo):.2f}€!!!")

def verificar_metas_risco()->list[str]:
    avisos = []
    metas = fetch("SELECT id, nome, valor_alvo, prazo FROM metas WHERE concluida = 0 AND prazo IS NOT NULL")
    poupancas = _poupancas_atuais()
    media = _media_poupancas_mensal()

    for id_,nome,valor_alvo,prazo in metas:
        valor_alvo = float(valor_alvo)
        falta = max(0.0,valor_alvo- poupancas)
        if falta<=0:
            continue
        meses_rest =_meses_ate(str(prazo))
        por_mes = falta / meses_rest
        if media <por_mes *0.8:
            avisos.append(f"Meta '{nome}': precisas {por_mes:.2f}€/mês, poupas {media:.2f}€/mês")
    return avisos

def painel_metas_dashboard() -> list[dict]:
    metas     = fetch("SELECT id, nome, valor_alvo, prazo FROM metas WHERE concluida = 0")
    poupancas = _poupancas_atuais()
    resultado = []
 
    for id_, nome, valor_alvo, prazo in metas:
        valor_alvo = float(valor_alvo)
        pct        = min(poupancas / valor_alvo * 100, 100) if valor_alvo > 0 else 0
        falta      = max(0.0, valor_alvo - poupancas)
        resultado.append({
            "nome":       nome,
            "valor_alvo": valor_alvo,
            "poupancas":  poupancas,
            "pct":        pct,
            "falta":      falta,
            "prazo":      str(prazo) if prazo else None,
        })
 
    return resultado
