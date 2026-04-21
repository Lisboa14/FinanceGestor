import re 
import unicodedata
import datetime 

from db import fetch
from orcamento import orcamento_dashboard
from despesas import total_despesas

def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

INTENCOES = {
    "total_mes_atual":[
        r"quanto gastei (este mes|este|no mes|no mes atual)",
        r"total (do|deste|no) mes",
        r"gastos (do|deste|no) mes",
        r"quanto gastei",
        r"total de gastos",
    ],
    "total_categoria":[
        r"quanto gastei em (\w+)",
        r"gastos em (\w+)",
        r"total (em|de|na|no) (\w+)",
        r"quanto foi em (\w+)",
    ],
    "maior_gasto":[
        r"maior gasto",
        r"despesa mais (alta|elevado|grande)",
        r"quanto foi o maximo",
        r"despesa maior",
        r"gasto mais alto",
    ],
    "menor_gasto":[
        r"menor gasto",
        r"despesa mais (baixa|barata|pequena)",
        r"gasto mais baixo",
        r"despesa menor",        
    ],
    "orcamento_estado":[
        r"(estou|eu estou) (dentro|fora) do orcamento",
        r"como (esta|anda) o (meu )? orcamento",
        r"quanto (me|tenho)? (resta|restante|disponivel)",
        r"(tenho|quanto tenho) disponivel",
        r"estado do orçamento",
        r"orçamento",
    ],
    "media_categoria":[
        r"media (em|de|na|no) (\w+)",
        r"quanto gasto em media (em|de|na|no) (\w+)",
        r"media de gastos em (\w+)",
    ],
    "mes_mais_caro":[
        r"mes mais caro",
        r"qual (foi o|o) mes (em que mais gastei|mais caro)",
        r"quando gastei mais",
        r"mes com mais gastos",
    ],
    "categoria_mais_cara":[
        r"(categoria|area) (onde|em que) (mais gastei| gastei mais)",
        r"onde gastei mais",
        r"categoria mias cara",
        r"maior categoria",
        r"em que categoria gastei mais",
    ],
    "num_despesas":[
        r"quantas despesas",
        r"numero de despesas",
        r"quantos gastos",
        r"quantas compras",
    ],
    "ultimo_gasto":[
        r"ultimo gasto",
        r"ultima despesa",
        r"(o que|qual foi) (o ultimo|a ultima) (gasto|despesa|compra)",
        r"ultima compra",
    ],
    "total_ano":[
        r"quanto gastei (este ano|no ano| em \d{4})",
        r"total (do|deste|no) ano",
        r"gastos (do|deste|no) ano",
        r"total anual",
    ],
    "poupancas_atuais":[
        r"(quanto|minhas|as minhas) poupanças",
        r"quanto poupei",
        r"total (de|das|em) poupanças",
        r"saldo (de|das) poupanças",
    ],
    "ajuda":[
        r"ajuda",
        r"help",
        r"o que (podes|posso|consigo) perguntar",
        r"que perguntas",
        r"exemplos",
        r"comandos",
    ],
}
def _total_mes_atual() -> str:
    mes=datetime.datetime.now().strftime("%Y-%m")
    sql = """
    SELECT SUM(valor) FROM despesas
    WHERE DATE_FORMAT(data,'%Y-%m') = %s 
    """
    total = fetch(sql, (mes,))[0][0] or 0
    return f"Gastaste {float(total):.2f}€ este mês ({mes})."

def _total_categoria(texto_original:str, match)->str:
    grupos = [g for g in match.groups() if g and len(g)>2]
    if not grupos:
        return "Não percebi a categoria. Tenta: 'quanto gastei em alimentação?'"
    categoria = grupos[-1]
    
    sql = """
    SELECT SUM(d.valor), c.nome FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    WHERE LOWER(c.nome) LIKE %s 
    LIMIT 1
    """

    resultado = fetch(sql,(f"%{categoria}%",))
    if not resultado:
        return f"Não encontrei gastos na categoria '{categoria}'."
    total, nome = resultado[0]
    return f"Gastaste {float(total):.2f}€ em {nome}."

def _maior_gasto()->str:
    sql = """
    SELECT d.valor, c.nome, d.descricao, d.data FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    ORDER BY d.valor DESC LIMIT 1
    """
    resultado = fetch(sql)
    if not resultado:
        return "Ainda não tens despesas registadas."
    v,cat,desc,data = resultado[0]
    return f"O teu maior gasto foi '{desc}' - {float(v):.2f}€ em {cat} ({data})."

def _menor_gasto()->str:
    sql = """
    SELECT d.valor, c.nome, d.descricao, d.data FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    ORDER BY d.valor ASC LIMIT 1
    """
    resultado = fetch(sql)
    if not resultado:
        return "Ainda não tens despesas registadas."
    v,cat,desc,data = resultado[0]
    return f"O teu menor gasto foi '{desc}' - {float(v):.2f}€ em {cat} ({data})."

def _orcamento_estado()-> str:
    restante = orcamento_dashboard()
    if restante is None:
        return "Não tens orçamento definido para este mês. Usa a opção [4] do teu menu."
    restante = float(restante)
    gasto = float(total_despesas() or 0)
    orcamento_val = gasto + restante
    estado = "dentro" if restante >= 0 else "Fora"
    emoji = "✅" if restante >= 0 else "❌"
    return (
        f"{emoji} Estás {estado} do orçamento.\n"
            f"Orçamento: {orcamento_val:.2f}€ | Gasto: {gasto:.2f}€ | Dispobível: {restante:.2f}€"
    )

def _media_categoria(match) -> str:
    grupos=[g for g in match.groups() if g and len(g)>2]
    if not grupos:
        return "Não percebi a categoria. Tenta: 'média em alimentação?'"
    categoria = grupos[-1]

    sql = """
    SELECT AVG(d.valor), c.nome FROM despesas d
    JOIN categorias c ON d.categoria_id = c.id 
    WHERE LOWER(c.nome) LIKE %s 
    GROUP BY c.nome
    LIMIT 1
    """
    resultado = fetch(sql,(f"%{categoria}%",))
    if not resultado:
        return f"Não encontrei gastos na categoria '{categoria}'."
    media, nome = resultado[0]
    return f"A tua média de gastos em {nome} é {float(media):.2f}€ por despesa."

def _mes_mais_caro()->str:
    sql = """
    SELECT DATE_FORMAT(data, '%Y-%m') as mes, SUM(valor) as total
    FROM despesas
    GROUP BY mes 
    ORDER BY total DESC 
    LIMIT 1
    """
    
    resultado = fetch(sql)
    if not resultado:
        return "Ainda não tens despesas registadas"
    mes, total = resultado[0]
    return f"O teu mês mais caro foi {mes} com {float(total):.2f}€ gastos."

def _categoria_mais_cara()->str:
    sql = """
    SELECT c.nome, SUM(d.valor) as total FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    GROUP BY c.nome 
    ORDER BY total DESC
    LIMIT 1
    """

    resultado = fetch(sql)
    if not resultado:
        return "Ainda não tens despesas registadas"
    nome,total = resultado[0]
    return f"A categoria onde gastas mais é '{nome}' com {float(total):.2f}€ no total."

def _num_despesas()->str:
    mes = datetime.datetime.now().strftime("%Y-%m")
    sql_mes="SELECT COUNT(*) FROM despesas WHERE DATE_FORMAT(data, '%Y-%m') = %s"
    sql_total="SELECT COUNT(*) FROM despesas"
    n_mes = fetch(sql_mes, (mes,))[0][0]
    n_total = fetch(sql_total)[0][0]
    return f"Tens {n_mes} despesas este mês e {n_total} despesas no total."

def _ultimo_gasto()->str:
    sql = """
    SELECT d.valor, c.nome, d.descricao, d.data FROM despesas d 
    JOIN categorias c ON d.categoria_id=c.id 
    ORDER BY d.data DESC, d.id DESC
    LIMIT 1
    """

    resultado = fetch(sql)
    if not resultado:
        return"Ainda não tens despesas registadas"
    v,cat,desc,data = resultado[0]
    return f"O teu último gasto foi '{desc}' - {float(v):.2f}€ em {cat} ({data})."

def _total_ano()->str:
    ano= datetime.datetime.now().year 
    sql = """
    SELECT SUM(valor) FROM despesas
    WHERE YEAR(data) = %s 
    """
    total = fetch(sql, (ano,))[0][0] or 0 
    return f"Gastaste {float(total):.2f}€ em {ano} no total."

def _poupancas_atuais()->str:
    mes = datetime.datetime.now().strftime("%Y-%m")
    sql = "SELECT valor FROM poupancas WHERE mes = %s"
    resultado = fetch(sql,(mes,))
    if not resultado:
        return "Ainda não há registos de poupancas para este mês."
    return f"As tuas poupancas acumuladas até este mês são {float(resultado[0][0]):.2f}€."

def _ajuda()->str:
    return (
        "Podes perguntar-me coisas como:\n"
        " *'quanto gastei este mês?'\n"
        " *'quanto gastei em alimentação?'\n"
        " *'qual foi o maior gasto?'\n"
        " *'estou dentro do orçamento?'\n"
        " *'média em transportes'\n"
        " *'qual o mês mais caro?'\n"
        " *'onde gasto mais?'\n"
        " *'quantas despesas tenho?'\n"
        " *'último gasto'\n"
        " *'total do ano'\n"
        " *'quanto poupei?'"
    )

def interpretar(pergunta: str) ->str:
    texto = normalizar(pergunta)

    for intencao, padroes in INTENCOES.items():
        for padrao in padroes:
            match = re.search(padrao,texto)
            if match:
                try:
                    return _executar(intencao, match,pergunta)
                except Exception as e:
                    return f"Ocorreu um erro ao processao: {e}"
    return(
        "Não percebi a pergunta.\n"
        "Escreve 'ajuda' para ver exemplos do que podes perguntar."
    )

def _executar(intencao: str, match, texto_original: str) -> str:
    if intencao == "total_mes_atual":
        return _total_mes_atual()
    elif intencao == "total_categoria":
        return _total_categoria(texto_original, match)
    elif intencao == "maior_gasto":
        return _maior_gasto()
    elif intencao == "menor_gasto":
        return _menor_gasto()
    elif intencao == "orcamento_estado":
        return _orcamento_estado()
    elif intencao == "media_categoria":
        return _media_categoria(match)
    elif intencao == "mes_mais_caro":
        return _mes_mais_caro()
    elif intencao == "categoria_mais_cara":
        return _categoria_mais_cara()
    elif intencao == "num_despesas":
        return _num_despesas()
    elif intencao == "ultimo_gasto":
        return _ultimo_gasto()
    elif intencao == "total_ano":
        return _total_ano()
    elif intencao == "poupancas_atuais":
        return _poupancas_atuais()
    elif intencao == "ajuda":
        return _ajuda()
    return "Não sei responder a isso ainda."
