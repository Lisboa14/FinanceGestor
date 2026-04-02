import plotext as plt 
import os 
from despesas import add_despesa, ver_despesas, total_despesas
from graficos import grafico_categorias

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
