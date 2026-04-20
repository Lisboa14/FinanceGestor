import re 
import unicodedata
import datetime 

from db import fetch
from orcamento import orcamento_dashboard
from despesas import total_despesas

def normalizar(texto: str)-> str:
    texto = texto.lower().strip()
    texto =".join(
        c for c in unicodedata.normalize('NFC' ,texto)
        if unicodedata.category(c) != 'Mn'
    )
    texto = re.sub(r'[^\w\s]',",texto)
    return texto 

INTENCOES = (
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
)
    
