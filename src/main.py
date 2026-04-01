import csv 
import datetime 

FILE = "../data/despesas.csv"
Categorias = ["Compras","Transporte","Lazer","Saúde"]
## Funções
def add_despesa():
    montante = float(input("Valor (€): "))

    print(f"Categorias disponíveis: {', '.join(Categorias)}")

    while True:
        categoriaEscolhida = input("Escolha uma categoria:")
        if categoriaEscolhida in Categorias:
            break
        else:
            print("Categoria inválida!!!")

    descricao = input("Descrição: ")
    data =datetime.datetime.now().strftime("%d/%m/%Y")
   
    file = open(FILE,"a", newline="")
    escrever = csv.writer(file)
    escrever.writerow([montante, categoriaEscolhida, descricao,data])
    file.close()

    print("Despesa adicionada com sucesso!!!")

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
def main():
    while True:
        print("****** Gestor de finanças *******")
        print("1-) Adicionar despesa")
        print("2-) Ver despesas")
        print("3-) Ver total de despesas")
        print("0-) Sair do programa")

        escolha = input("Escolha: ")

        if escolha == "1":
            add_despesa()
        elif escolha== "2":
            ver_despesas()
        elif escolha== "3":
            total_despesas()
        elif escolha == "0":
            print("\n Muito obrigado por utlizador o programa FinanceGestor\n")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
