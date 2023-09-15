
import sqlite3
# Crie o banco de dados e a tabela de usuários
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Crie uma tabela de usuários (você pode adicionar mais campos conforme necessário)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

