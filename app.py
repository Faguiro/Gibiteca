from flask import Flask, jsonify, render_template, request
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Substitua por uma chave secreta segura

login_manager = LoginManager()
login_manager.login_view = 'login'  # A rota para a página de login
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/api/login', methods=['POST'])
def api_login():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Conecte-se ao banco de dados
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        # Verifique se o usuário existe no banco de dados
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            # A senha fornecida corresponde à senha no banco de dados
            user_obj = User(user[0])
            login_user(user_obj)
            conn.close()
            return jsonify(success=True, message="Login bem-sucedido")

        conn.close()
        return jsonify(success=False, message="Credenciais inválidas")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Conecte-se ao banco de dados
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        # Verifique se o usuário existe no banco de dados
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            # A senha fornecida corresponde à senha no banco de dados
            user_obj = User(user[0])
            login_user(user_obj)
            conn.close()
            return redirect(url_for('index'))

        conn.close()
        return 'Credenciais inválidas'

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/logout')
@login_required
def logout_api():
    logout_user()
    return jsonify(success=True, message="Logouts bem-sucedido")

# ...

@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Conecte-se ao banco de dados
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        # Verifique se o nome de usuário já existe no banco de dados
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return 'Nome de usuário já registrado'

        # Se o nome de usuário não existe, crie um novo usuário
        hashed_password = generate_password_hash(password, method='sha256')
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# ...

@app.route('/api/palavraschave', methods=['GET'])
def obter_palavras_chave():
    try:
        with open('resultados.json', 'r') as arquivo_json:
            dados = json.load(arquivo_json)
        return jsonify(dados)
    except FileNotFoundError:
        return "Arquivo 'resultados.json' não encontrado", 404


@app.route('/comics')
def get_comics():
    page = request.args.get('page', default=1, type=int)
    per_page = 40
    offset = (page - 1) * per_page

    conn = sqlite3.connect("comics_data.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM comics LIMIT ? OFFSET ?''',
                   (per_page, offset))
    comics = cursor.fetchall()
    conn.close()

    # Converter a lista de tuplas em uma lista de dicionários chave-valor
    comics_list = []
    for comic in comics:
        comic_dict = {
            'id': comic[0],
            'capa': comic[1],
            'editora': comic[2],
            'titulo': comic[3],
            'link': comic[4],
            'descricao': comic[5],
            'links_adicionais': comic[6]
        }
        comics_list.append(comic_dict)

    return jsonify(comics_list)


@app.route('/')
def index():
    user = current_user
    return render_template('index.html', user=user)


@app.route('/editora/<editora>')
def editora_comics(editora):
    page = request.args.get('page', default=1, type=int)
    per_page = 40
    offset = (page - 1) * per_page

    conn = sqlite3.connect("comics_data.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM comics WHERE editora = ? LIMIT ? OFFSET ?''',
                   (editora, per_page, offset))
    comics = cursor.fetchall()
    conn.close()

    comics_list = []
    for comic in comics:
        comic_dict = {
            'id': comic[0],
            'capa': comic[1],
            'editora': comic[2],
            'titulo': comic[3],
            'link': comic[4],
            'descricao': comic[5],
            'links_adicionais': comic[6]
        }
        # print(comic_dict)
        comics_list.append(comic_dict)

    return jsonify(comics_list)


@app.route('/comic_id')
def comic_id(_id):
    conn = sqlite3.connect("comics_data.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM comics WHERE id = ?''', (_id,))
    comic = cursor.fetchone()
    conn.close()

    comic_dict = {
        'id': comic[0],
        'capa': comic[1],
        'editora': comic[2],
        'titulo': comic[3],
        'link': comic[4],
        'descricao': comic[5],
        'links_adicionais': comic[6]
    }

    return jsonify(comic_dict)


@app.route('/comic/<int:_id>')
def comic(_id):
    conn = sqlite3.connect("comics_data.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM comics WHERE id = ?''', (_id,))
    comic = cursor.fetchone()
    conn.close()

    user = current_user
    try:
        if user.id:links_adicionais = comic[6].split('\n')
        else: links_adicionais =["Faça login para acessar os links: /login"]  
    except:
        links_adicionais =["Faça login para acessar os links: /login"]


    comic_dict = {
        'id': comic[0],
        'capa': comic[1],
        'editora': comic[2],
        'titulo': comic[3],
        'link': comic[4],
        'descricao': comic[5],
        'links_adicionais': links_adicionais # Use a lista de links aqui
    }

    return render_template('comic.html', comic=comic_dict)


@app.route('/search/<keyword>')
@login_required
def search(keyword):
    if not keyword:
        return render_template('index.html')
    return render_template('search.html', keyword=keyword)


@app.route('/search')
def search_comics():
    keyword = request.args.get('keyword')
    if not keyword:
        return render_template('index.html')
    page = request.args.get('page', type=int, default=1)
    per_page = 12  # Defina o número de resultados por página
    offset = (page - 1) * per_page

    conn = sqlite3.connect("comics_data.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM comics WHERE titulo LIKE ? LIMIT ? OFFSET ?''',
                   ('%' + keyword + '%', per_page, offset))
    comics = cursor.fetchall()
    conn.close()

    comics_list = []
    for comic in comics:
        comic_dict = {
            'id': comic[0],
            'capa': comic[1],
            'editora': comic[2],
            'titulo': comic[3],
            'link': comic[4],
            'descricao': comic[5],
            'links_adicionais': comic[6]
        }
        comics_list.append(comic_dict)

    return jsonify(comics_list)


@app.route('/search_info')
def search_info():
    keyword = request.args.get('keyword')

    conn = sqlite3.connect("comics_data.db")
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT COUNT(*) FROM comics WHERE titulo LIKE ?''', ('%' + keyword + '%',))
    total_results = cursor.fetchone()[0]
    conn.close()

    per_page = 12  # Defina o número de resultados por página
    # Calcula o total de páginas
    total_pages = (total_results + per_page - 1) // per_page

    info = {
        'total_results': total_results,
        'total_pages': total_pages
    }

    return jsonify(info)

@app.route('/search_all')
def search_all():
    

    conn = sqlite3.connect("comics_data.db")
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT COUNT(*) FROM comics ''')
    total_results = cursor.fetchone()[0]
    conn.close()

    per_page = 12  # Defina o número de resultados por página
    # Calcula o total de páginas
    total_pages = (total_results + per_page - 1) // per_page

    info = {
        'total_results': total_results,
        'total_pages': total_pages
    }

    return jsonify(info)


@app.route('/dc_comics')
def dc_comics():
    return render_template('editora.html', comics=editora_comics('DC Comics'), editora='DC Comics')


@app.route('/marvel_comics')
def marvel_comics():
    return render_template('editora.html', comics=editora_comics('Marvel Comics'), editora='Marvel Comics')


@app.route('/other_comics')
def other_comics():
    return render_template('editora.html', comics=editora_comics('Other Comics'), editora='Other Comics')


if __name__ == '__main__':
    app.run(debug=True)
