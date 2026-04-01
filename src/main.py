import csv 
import datetime 

FILE = "../data/despesas.csv"
## Funções
def add_despesa():
    montante = float(input("Valor (€): "))
    categoria = input("Categoria: ")
    descricao = input("Descrição: ")
    data =datetime.datetime.now().strftime("%d/%m/%Y")
   
    file = open(FILE,"a", newline="")
    escrever = csv.writer(file)
    escrever.writerow([montante, categoria, descricao,data])
    file.close()

    print("Despesa adicionada com sucesso!!!")

def ver_despesas():
    file = open(FILE, "r")
    leitor=csv.reader(file)

    print("\n Lista de despesas: \n")

    for row in leitor:
        print(f"Despesa: {row[0]}€ | Categoria:{row[1]} | Descrição:{row[2]} | Data:{row[3]}")
    
    file.close()
def main():
    print("****** Gestor de finanças *******")
    print("1-) Adicionar despesa")
    print("2-) Ver despesas")

    escolha = input("Escolha: ")

    if escolha == "1":
       add_despesa()
    elif escolha== "2":
        ver_despesas()
    else:
        print("Opção inválida")

if __name__ == "__main__":
    main()
