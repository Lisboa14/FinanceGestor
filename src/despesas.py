import csv
import datetime 
FILE = "../data/despesas.csv"
FILECATEGORIAS = "../data/categorias.txt"

def add_despesa():
    montante = float(input("Valor (€): "))
    
    categorias= carregar_categorias()
    print("\n Categorias dispovineis")
    for categoria in categorias:
        print(f"->{categoria}")
    while True:
        categoriaEscolhida = input("Escolha uma categoria:")
        if categoriaEscolhida in categorias:
            break
        else:
            print("Categoria inválida!!!")
        
            opcao=input("Deseja criar uma nova categoria? (s/n)")

            if opcao == "s":
                with open(FILECATEGORIAS, "a") as f:
                   f.write(categoriaEscolhida + "\n") 
                print("Categoria Adicionada com sucesso!!!")
                break
            elif opcao== "n":
                print("Volta para o menu principal")
                return
            else:
                print("opcao inválida")

    descricao = input("Descrição: ")
    data =datetime.datetime.now().strftime("%d/%m/%Y")
   
    file = open(FILE,"a", newline="")
    escrever = csv.writer(file)
    escrever.writerow([montante, categoriaEscolhida, descricao,data])
    file.close()

    print("Despesa adicionada com sucesso!!!")

def carregar_categorias():
    categorias = []
    
    file2 = open(FILECATEGORIAS,"r")
    for linha in file2:
        categorias.append(linha.strip())
    return categorias

def ver_despesas():
    file = open(FILE, "r")
    leitor=csv.reader(file)

    print("\n Lista de despesas: \n")

    for row in leitor:
        print(f"Despesa: {row[0]}€ | Categoria:{row[1]} | Descrição:{row[2]} | Data:{row[3]}")
    
    file.close()

def total_despesas():
    total = 0;
    file = open(FILE, "r")
    leitor = csv.reader(file)
    for row in leitor:
        total+= float(row[0])
    file.close()

    print(f"\n Total de gastos: {total:.2f}€ \n")

