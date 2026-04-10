from db import fetch, execute
#import csv
import datetime 
#FILE = "../data/despesas.csv"
#FILECATEGORIAS = "../data/categorias.txt"

def add_despesa():
    montante = float(input("Valor (€): "))
    
    categorias= carregar_categorias()
    print("\n Categorias disponiveis:")
    for categoria in categorias:
        print(f"->{categoria}")
    while True:
        categoriaEscolhida = input("Escolha uma categoria:")
        if categoriaEscolhida in categorias:
            sql = "SELECT id FROM categorias WHERE nome=%s"
            categoria_id = fetch(sql,(categoriaEscolhida,))[0][0]
            break
        else:
            print("Categoria inválida!!!")
        
            opcao=input("Deseja criar uma nova categoria? (s/n)")

            if opcao == "s":
                execute("INSERT INTO categorias (nome) VALUES (%s)", (categoriaEscolhida,))
                print("Categoria Adicionada com sucesso!!!")
                categoria_id = fetch("SELECT id FROM categorias WHERE nome=%s", (categoriaEscolhida,))[0][0]
                break
            elif opcao== "n":
                print("Volta para o menu principal")
                return
            else:
                print("opcao inválida")

    descricao = input("Descrição: ")
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
    print(f"\n Total de gastos: {total:.2f}€ \n")

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

