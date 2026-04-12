import matplotlib.pyplot as plt 
import os
from db import fetch, execute
##import csv
##FILE = "../data/despesas.csv"

def grafico_categorias():
    totais = {}

    sql = """
    SELECT d.valor, c.nome 
    FROM despesas d 
    JOIN categorias c ON d.categoria_id = c.id 
    """
    resultados = fetch(sql)
    for row in resultados:
        valor=float(row[0])
        categoria = row[1]

        if categoria in totais:
            totais[categoria] += valor
        else:
            totais[categoria] = valor
    if not totais:
        print("Sem dados para mostrar")
        return
    categorias = list(totais.keys())
    valores = list(totais.values())

    plt.pie(valores, labels=categorias, autopct='%1.1f%%')
    plt.title("Gráfico Despesa por Categorias")
    plt.xlabel("Categorias")
    plt.show()
