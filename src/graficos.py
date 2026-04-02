import plotext as plt 
import os 
import csv
FILE = "../data/despesas.csv"

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
