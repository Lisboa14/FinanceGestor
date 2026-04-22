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
