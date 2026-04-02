import csv 
import datetime 
import plotext as plt 
import os 
FILE = "../data/despesas.csv"
FILECATEGORIAS = "../data/categorias.txt"
#Categorias = ["Compras","Transporte","Lazer","Saúde"]
## Funções
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

def grafico_categorias():
    totais = {}

    with open(FILE,"r") as file:
        leitor = csv.reader(file)

        for row in leitor:
            categoria = row[1]
            valor=float(row[0])

            if categoria in totais:
                totais[categoria] += valor
            else:
                totais[categoria] = valor
    if not totais:
        print("Sem dados para mostrar")
        return
    categorias = list(totais.keys())
    valores = list(totais.values())

    plt.clear_figure()
    plt.bar(categorias, valores)
    plt.title("Gráfico Despesa por Categorias")
    plt.xlabel("Categorias")
    plt.show()
def limpar_terminal():
    os.system('cls' if os.name=='nt' else 'clear')
def main():
    while True:
        print("****** Gestor de finanças *******")
        print("1-) Adicionar despesa")
        print("2-) Ver despesas")
        print("3-) Ver total de despesas")
        print("4-) Ver gráficos por categorias")
        print("0-) Sair do programa")

        escolha = input("Escolha: ")
        limpar_terminal()

        if escolha == "1":
            add_despesa()
        elif escolha== "2":
            ver_despesas()
        elif escolha== "3":
            total_despesas()
        elif escolha == "4":
            grafico_categorias()
        elif escolha == "0":
            print("\n Muito obrigado por utilizar o programa FinanceGestor\n")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
