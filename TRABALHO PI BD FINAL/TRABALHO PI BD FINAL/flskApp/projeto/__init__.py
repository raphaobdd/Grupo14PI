from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import DB_CONFIG
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = DB_CONFIG['MYSQL_HOST']
app.config['MYSQL_USER'] = DB_CONFIG['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = DB_CONFIG['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = DB_CONFIG['MYSQL_DB']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('register_page.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form.get('user')
        senha = request.form.get('password')
        confirma_senha = request.form.get('confirmar_senha')
        cursor = mysql.connection.cursor()
        if not usuario or not senha or not confirma_senha:
            flash('Todos os campos são obrigatórios!', 'error')
            return render_template('/register_page.html/')
        if len(senha) > 8:
            flash('Senha deve ter no máximo 8 caracteres!', 'error')
            return render_template('/register_page.html/')
        if senha != confirma_senha:
            flash('Senhas não conferem!', 'error')
            return render_template('/register_page.html/')
        try:
            cursor.execute("SELECT * FROM login WHERE user = %s", [usuario])
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Usuário já cadastrado!', 'error')
                return render_template('/register_page.html/')
            cursor.execute("INSERT INTO login (user, password) VALUES (%s, %s)", (usuario, senha))
            mysql.connection.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Erro de cadastro: {e}")
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
            return render_template('/register_page.html/')
        finally:
            cursor.close()
    return render_template('/register_page.html/')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/login_page.html/')
    username = request.form['user']
    password = request.form['password']
    if not username or not password:
        flash('Usuário e senha são obrigatórios', 'error')
        return render_template('/login_page.html/')
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM login WHERE user = %s", [username])
        result = cur.fetchone()
        if result and result[0] == password:
            session['username'] = username
            return redirect(url_for('busca'))
        else:
            flash('Usuário ou senha incorretos', 'error')
            return render_template('/login_page.html/')
    except Exception as e:
        print(f"Erro de login: {e}")
        flash('Erro interno. Tente novamente.', 'error')
        return render_template('/login_page.html/')
    finally:
        cur.close()

@app.route('/busca/', methods=['GET', 'POST'])
def busca():
    if request.method == 'POST':
        nome_industria = request.form['empresa']
        if not nome_industria:
            flash("Nome da empresa não pode ser vazio!")
            return render_template('search_page.html')
        
        try:
            cur = mysql.connection.cursor()
            search_term = f"%{nome_industria}%"
            print(f"Searching for: {search_term}")  
            
            cur.execute("SELECT nome FROM industria WHERE nome LIKE %s", (search_term,))
            empresa = cur.fetchone()
            
            print(f"Query result: {empresa}")  
            
            if empresa:
                print("Empresa encontrada!") 
                return redirect(url_for('principal'))
            else:
                flash("Empresa não encontrada!")
                return render_template('search_page.html')
        
        except Exception as e:
            print(f"Erro na busca: {e}")
            flash(f"Erro ao buscar empresa: {e}")
            return render_template('search_page.html')
        
        finally:
            if 'cur' in locals():
                cur.close()
    
    return render_template('search_page.html')

@app.route('/principal', methods=['GET', 'POST'])
def principal():
    try:
        cur = mysql.connection.cursor()
        
        # Consulta para buscar todas as indústrias com seus dados de emissão
        cur.execute("""
            SELECT i.id, i.nome, i.pais_sede, i.faturamento_anual, 
                i.numero_empregados, 
                e.volume_emissao, e.ferramentas_reducao, 
                e.tipo_descarte
            FROM industria i
            LEFT JOIN emissoes e ON i.id = e.industria_id
            ORDER BY i.nome
        """)
        
        # Busca todos os resultados
        results = cur.fetchall()
        
        # Converte resultados para uma lista de dicionários
        industrias = []
        for row in results:
            industria = {
                'id': row[0],
                'nome': row[1],
                'pais_sede': row[2],
                'faturamento_anual': row[3],
                'numero_empregados': row[4],
                'emissoes': {
                    'volume_emissao': row[5],
                    'ferramentas_reducao': row[6],
                    'tipo_descarte': row[7]
                } if row[5] else None
            }
            industrias.append(industria)
        
        # Close the cursor before returning
        cur.close()
        
        # Renderiza o template com os dados
        return render_template('main_page.html', industrias=industrias)
    
    except Exception as e:
        # Tratamento de erro
        print(f"Erro na consulta: {e}")
        flash(f"Erro ao consultar dados: {e}", 'error')
        return render_template('main_page.html'), 500

@app.route('/inserir', methods=['GET', 'POST'])
def inserir():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            pais_sede = request.form['pais_sede']
            faturamento_anual = request.form['faturamento_anual']
            numero_empregados = request.form['numero_empregados']

            volume_emissao = request.form['volume_emissao']
            ferramentas_reducao = request.form['ferramentas_reducao']
            substancia_descarte = request.form['substancia_descarte']
            
            if not nome or not pais_sede or not volume_emissao:
                flash("Campos obrigatórios não podem estar vazios!")
                return render_template('insert_page.html')  # Changed this line
            
            cur = mysql.connection.cursor()

            cur.execute("""
                INSERT INTO industria 
                (nome, pais_sede, faturamento_anual, numero_empregados) 
                VALUES (%s, %s, %s, %s)
            """, (nome, pais_sede, faturamento_anual, numero_empregados))
            
            industria_id = cur.lastrowid
            
            cur.execute("""
                INSERT INTO emissoes 
                (industria_id, volume_emissao, ferramentas_reducao, tipo_descarte) 
                VALUES (%s, %s, %s, %s)
            """, (industria_id, volume_emissao, ferramentas_reducao, substancia_descarte))
            
            mysql.connection.commit()
            
            flash("Cadastro de industria realizado com sucesso!")
            return redirect(url_for('busca'))
        
        except Exception as e:
            mysql.connection.rollback()
            print(f"Erro no cadastro: {e}")
            flash(f"Erro ao cadastrar: {e}")
            return render_template('insert_page.html') 
        
        finally:
            if 'cur' in locals():
                cur.close()
    
    return render_template('insert_page.html')

if __name__ == '__main__':
    app.secret_key = 'chave_secreta'
    app.run(debug=True)
