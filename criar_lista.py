import json
import sqlite3
import re

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('comics_data.db')
cursor = conn.cursor()

# Consulta SQL para obter todos os títulos da tabela 'comics'
sql = "SELECT titulo FROM comics"
cursor.execute(sql)

# Inicializa um dicionário para armazenar a contagem de palavras
contagem_palavras = {}

# Função para dividir o texto em palavras
def dividir_em_palavras(texto):
    palavras = re.findall(r'\b\w{4,}\b', texto.lower())
    return palavras

# Loop através dos títulos e contar as palavras
for row in cursor.fetchall():
    titulo = row[0]
    palavras = dividir_em_palavras(titulo)
    
    for palavra in palavras:
        if palavra in contagem_palavras:
            contagem_palavras[palavra] += 1
        else:
            contagem_palavras[palavra] = 1

# Ordenar o dicionário com base nos valores em ordem decrescente
resultados_ordenados = dict(sorted(contagem_palavras .items(), key=lambda item: item[1], reverse=True))

# Salva os resultados em um arquivo JSON
with open('resultados.json', 'w', encoding='utf-8') as json_file:
    json.dump(resultados_ordenados, json_file, ensure_ascii=False, indent=4)

# Fecha a conexão com o banco de dados
conn.close()

print("Contagem de palavras concluída e resultados salvos em 'resultados.json'.")
