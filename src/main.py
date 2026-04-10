import plotext as plt 
import os 
from despesas import add_despesa, ver_despesas, total_despesas, ver_despesas_categoria, ver_despesas_mes, ver_despesas_data
from graficos import grafico_categorias
from orcamento import definir_orcamento, ver_orcamento, orcamento_dashboard

def limpar_terminal():
    os.system('cls' if os.name=='nt' else 'clear')
def main():
    while True:
        restante = orcamento_dashboard()
        print("****** Gestor de finanças *******")
        print(f"Orçamento deste mês: {restante}€\n")
        print("1-) Adicionar despesa")
        print("2-) Ver despesas")
        print("3-) Ver gráficos por categorias")
        print("4-) Definir orçamento")
        print("5-) Ver orçamento mensal")
        print("0-) Sair do programa")

        escolha = input("Escolha: ")
        limpar_terminal()

        if escolha == "1":
            add_despesa()
        elif escolha== "2":
            menu_ver_despesas()
        elif escolha == "3":
            grafico_categorias()
        elif escolha == "4":
            definir_orcamento()
        elif escolha == "5":
            ver_orcamento()
        elif escolha == "0":
            print("\n Muito obrigado por utilizar o programa FinanceGestor\n")
            break
        else:
            print("Opção inválida")

def menu_ver_despesas():
    while True:
        print("\n *** Ver Despesas ***")
        print("1-) Ver Todos")
        print("2-) Por Categoria")
        print("3-) Por Mês")
        print("4-) Por Data Especifica")
        print("0-) Voltar")

        escolha = input("Escolha: ")
        limpar_terminal()

        if escolha == "1":
            ver_despesas()
        elif escolha == "2":
            ver_despesas_categoria()
        elif escolha == "3":
            ver_despesas_mes()
        elif escolha == "4":
            ver_despesas_data()
        elif escolha == "0":
            break 
        else:
            print("Opção Inválida")

if __name__ == "__main__":
    main()
