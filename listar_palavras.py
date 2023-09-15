import json
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('comics_data.db')
cursor = conn.cursor()

# Consulta SQL para contar as palavras no campo 'titulo' com mais de 3 letras
sql = """
    SELECT palavra, COUNT(palavra) AS quantidade
    FROM (
        SELECT SUBSTR(titulo, 4) AS palavra
        FROM (
            SELECT DISTINCT titulo
            FROM comics
            WHERE LENGTH(titulo) > 3
        )
    ) p
    GROUP BY palavra
"""

cursor.execute(sql)

# Cria um dicionário com os resultados
resultado = {}
for row in cursor.fetchall():
    palavra, quantidade = row
    resultado[palavra] = quantidade

# Salva os resultados em um arquivo JSON
with open('resultados.json', 'w', encoding='utf-8') as json_file:
    json.dump(resultado, json_file, ensure_ascii=False, indent=4)

# Fecha a conexão com o banco de dados
conn.close()

print("Contagem de palavras concluída e resultados salvos em 'resultados.json'.")
