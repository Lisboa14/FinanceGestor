import matplotlib.pyplot as plt 
import os
from db import fetch, execute
from datetime import datetime 

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

def grafico_intervalo():
    data_inicio = input("Data início (YYYY-MM-DD): ")
    data_fim = input("Data fim (YYYY-MM-DD): ")

    try:
        inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        fim = datetime.strptime(data_fim, "%Y-%m-%d")
    except:
        print("Formato inválido. Usa YYYY-MM-DD")
        return 
    if inicio > fim:
        print("Data início maior que a data fim")
        return
    
    sql = """
    SELECT DATE(data), SUM(valor)
    FROM despesas
    WHERE data BETWEEN %s AND %s 
    GROUP BY DATE(data)
    ORDER BY DATE(data)
    """

    resultados = fetch(sql, (data_inicio, data_fim))

    if not resultados:
        print("Sem dados para este intervalo")
        return
    
    datas = [str(r[0]) for r in resultados]
    totais = [float(r[1]) for r in resultados]

    plt.figure(figsize=(10,5))
    plt.plot(datas, totais, marker='o')
    plt.fill_between(datas, totais, alpha=0.1)
    plt.title(f"Gastos de {data_inicio} até {data_fim}")
    plt.xticks(rotation=45)
    plt.ylabel("€")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
