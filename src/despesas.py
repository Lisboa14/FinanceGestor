from db import fetch, execute
#import csv
import datetime 
#FILE = "../data/despesas.csv"
#FILECATEGORIAS = "../data/categorias.txt"
import re 
import unicodedata

KEYWORDS_PADRAO = {
    # Alimentação
    "continente": "Alimentação", "pingo doce": "Alimentação", "lidl": "Alimentação",
    "aldi": "Alimentação", "mercadona": "Alimentação", "minipreço": "Alimentação",
    "intermarché": "Alimentação", "supermercado": "Alimentação", "mercearia": "Alimentação",
    "padaria": "Alimentação", "talho": "Alimentação", "feira": "Alimentação",
 
    # Restaurantes
    "restaurante": "Restaurantes", "café": "Restaurantes", "mcdonalds": "Restaurantes",
    "kfc": "Restaurantes", "burger king": "Restaurantes", "pizza": "Restaurantes",
    "sushi": "Restaurantes", "tasca": "Restaurantes", "snack": "Restaurantes",
    "almoço": "Restaurantes", "jantar": "Restaurantes", "takeaway": "Restaurantes",
 
    # Transportes
    "gasolina": "Transportes", "combustível": "Transportes", "uber": "Transportes",
    "bolt": "Transportes", "táxi": "Transportes", "autocarro": "Transportes",
    "metro": "Transportes", "comboio": "Transportes",
    "portagem": "Transportes", "via verde": "Transportes", "estacionamento": "Transportes",
 
    # Saúde
    "farmácia": "Saúde", "médico": "Saúde", "consulta": "Saúde", "dentista": "Saúde",
    "hospital": "Saúde", "clínica": "Saúde", "análises": "Saúde", "exame": "Saúde",
    "medicamento": "Saúde", "óculos": "Saúde",
 
    # Subscrições
    "netflix": "Subscrições", "spotify": "Subscrições", "youtube": "Subscrições",
    "amazon prime": "Subscrições", "hbo": "Subscrições", "disney": "Subscrições",
    "apple": "Subscrições", "adobe": "Subscrições", "microsoft": "Subscrições","dazn": "Subscrições",
 
    # Telecomunicações
    "nos": "Telecomunicações", "meo": "Telecomunicações", "vodafone": "Telecomunicações",
    "nowo": "Telecomunicações", "internet": "Telecomunicações", "telemóvel": "Telecomunicações",
 
    # Habitação
    "renda": "Habitação", "condomínio": "Habitação", "água": "Habitação",
    "luz": "Habitação", "gás": "Habitação", "eletricidade": "Habitação",
    "edp": "Habitação", "endesa": "Habitação",
 
    # Lazer
    "cinema": "Lazer", "teatro": "Lazer", "concerto": "Lazer", "museu": "Lazer",
    "ginásio": "Lazer", "gym": "Lazer", "viagem": "Lazer", "hotel": "Lazer",
    "airbnb": "Lazer", "bilhete": "Lazer", "jogo": "Lazer",
 
    # roupa
    "zara": "roupa", "pull&bear": "roupa", "roupa": "roupa", "sapatos": "roupa",
    "decathlon": "roupa",
 
    # Educação
    "escola": "Educação", "universidade": "Educação", "curso": "Educação",
    "livro": "Educação", "propinas": "Educação", "explicação": "Educação",
    "material escolar": "Educação",
}
def normalizar(texto : str) -> str:
    texto = texto.lower()

    texto = unicodedata.normalize("NFD", texto)
    texto ="".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^\w\s]", "", texto)

    return texto 

def add_despesa():
    criar_tabela_keywords()
    montante = float(input("Valor (€): "))
    
    descricao = input("Descrição: ").strip()
    
    categoria_id = escolher_categoria(descricao)
    if categoria_id is None:
        return 

    data =datetime.datetime.now().strftime("%Y-%m-%d")
    sql = "INSERT INTO despesas (data,categoria_id, descricao, valor) VALUES (%s,%s,%s,%s)"
    execute(sql,(data, categoria_id, descricao, montante))
    print("Despesa adicionada com sucesso!!!")

def carregar_categorias():
    sql = "SELECT nome FROM categorias"
    categorias = [c[0] for c in fetch(sql)]
    return categorias

def ver_despesas():
    sql = """
        SELECT d.valor, c.nome, d.descricao, d.data
        FROM despesas d 
        JOIN categorias c ON d.categoria_id = c.id
    """
    despesas = fetch(sql)
        
    print("\nLista de despesas:\n")
    for d in despesas:
        print(f"Despesa: {d[0]:.2f}€ | Categoria: {d[1]} | Descrição: {d[2]} | Data: {d[3]}")

def total_despesas():
    sql = "SELECT SUM(valor) FROM despesas"
    total = fetch(sql)[0][0] or 0
    #print(f"\n Total de gastos: {total:.2f}€ \n")
    return total

def ver_despesas_categoria():
    
    categorias= carregar_categorias()
    print("\n Categorias disponiveis:")
    for categoria in categorias:
        print(f"->{categoria}")
   
    categoria = input("Escreva a Categoria: ")
    
    sql = """
    SELECT d.valor, c.nome, d.descricao, d.data
    FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id
    WHERE c.nome = %s 
    """
    despesas = fetch(sql ,(categoria,))

    print("\nLista de despesas:\n")
    if not despesas:
        print("Nenhuma disponivel nesta categoria")
    else:
        for d in despesas:
            print(f"Despesa: {d[0]:.2f}€ | Categoria: {d[1]} | Descrição: {d[2]} | Data: {d[3]}")
def ver_despesas_mes():
    mes = input("Mês (1-12)")

    sql = """
    SELECT d.valor, c.nome, d.descricao, d.data
    FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    WHERE MONTH(d.data) = %s 
    """
    despesas = fetch(sql,(mes,))
    if not despesas:
        print("Nenhuma disponivel neste mês")
    else:
        for d in despesas:
            print(f"Despesa: {d[0]:.2f}€ | Categoria: {d[1]} | Descrição: {d[2]} | Data: {d[3]}")
def ver_despesas_data():
    data = input("Data (YYYY-MM-DD): ")
    
    sql = """
    SELECT d.valor, c.nome, d.descricao, d.data
    FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    WHERE d.data = %s 
    """
    despesas = fetch(sql,(data,))
    
    print("\nLista de despesas:\n")
    if not despesas:
        print("Nenhuma disponivel neste dia")
    else:
        for d in despesas:
            print(f"Despesa: {d[0]:.2f}€ | Categoria: {d[1]} | Descrição: {d[2]} | Data: {d[3]}")

    
def criar_tabela_keywords():
    sql = """
    CREATE TABLE IF NOT EXISTS palavra_chave(
        id INT AUTO_INCREMENT PRIMARY KEY,
        palavra VARCHAR(100) UNIQUE NOT NULL,
        categoria_id INT NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """
    execute(sql)
    
def sugerir_categoria(descricao: str) -> str | None:
    descricao_lower = normalizar(descricao)

    sql = """
    SELECT c.nome FROM palavra_chave pk
    JOIN categorias c ON pk.categoria_id = c.id 
    WHERE %s LIKE CONCAT('%%', pk.palavra, '%%')
    ORDER BY LENGTH(pk.palavra) DESC 
    LIMIT 1
    """
    resultado = fetch(sql, (descricao_lower,))
    if resultado:
        return resultado[0][0]
    
    for keyword, categoria in KEYWORDS_PADRAO.items():
        keyword_norm = normalizar(keyword)
        if keyword_norm in descricao_lower:
            return categoria
    return None

def aprender_keyword(descricao: str, categoria_id: int):
    palavra = descricao.lower().strip()[:100]
    if not palavra:
        return
    sql = """
    INSERT INTO palavra_chave (palavra, categoria_id)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE categoria_id = %s 
    """
    execute(sql,(palavra,categoria_id,categoria_id))

def escolher_categoria(descricao: str) ->int | None:
    categorias = carregar_categorias()
    sugestao = sugerir_categoria(descricao)

    if sugestao and sugestao in categorias:
        print(f"\n 🪄 Sugestão automática: [{sugestao}]")
        aceitar = input("Aceitar? (Enter para confirmar, 'n' para escolher outra): ").strip().lower()
        
        if aceitar != "n":
            sql = "SELECT id FROM categorias WHERE nome=%s"
            categoria_id = fetch(sql, (sugestao,))[0][0]
            aprender_keyword(descricao, categoria_id)
            return categoria_id

    print("\n Cateorias disponiveis: ")
    for categoria in categorias:
        marcador = "🪄 " if categoria == sugestao else "->"
        print(f" {marcador} {categoria}")
    
    while True:
        categoriaEscolhida = input("\n Escolha uma categoria: ").strip()

        if categoriaEscolhida in categorias:
            sql = "SELECT id FROM categorias WHERE nome=%s"
            categoria_id = fetch(sql, (categoriaEscolhida,))[0][0]

            aprender_keyword(descricao, categoria_id)
            return categoria_id
        
        print("Categoria inválida")
        opcao = input("  Deseja criar uma nova categoria? (s/n): ").strip().lower()
 
        if opcao == "s":
            execute("INSERT INTO categorias (nome) VALUES (%s)", (categoriaEscolhida,))
            print("  Categoria criada com sucesso!")
            categoria_id = fetch("SELECT id FROM categorias WHERE nome=%s", (categoriaEscolhida,))[0][0]
            aprender_keyword(descricao, categoria_id)
            return categoria_id
        elif opcao == "n":
            print("  A voltar ao menu principal...")
            return None
        else:
            print("  Opção inválida.")
def remover_despesa():
    sql = """
    SELECT d.id,d.valor,c.nome,d.descricao,d.data
    FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    """

    despesas = fetch(sql)

    if not despesas:
        print("Não há despesas para remover")
        return 
    print("\nLista de despesas\n")
    for d in despesas:
        print(f"[{d[0]}] {d[1]:.2f} | {d[2]} | {d[3]} | {d[4]}")
    try:
        id_despesa = int(input("\nID da despesa a remover: "))
    except:
        print("ID inválido")
        return 
    confirmar = input("Tens certeza que queres remover? (s/n): ").lower()
    if confirmar != "s":
        print("Cancelado.")
        return
    execute("DELETE FROM despesas WHERE id = %s",(id_despesa,))
    print("Despesa removida com sucesso!!!")

