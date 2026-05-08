import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações de Upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# URL da sua API FastAPI
API_BASE_URL = "http://localhost:8000"

# Garante que a pasta de uploads exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROTAS DE MODELOS ---

@app.route('/')
def index():
    tipo = request.args.get("filtro_tipo")
    valor = request.args.get("filtro_valor")
    filtros = {}
    if tipo and valor:
        filtros[tipo] = valor
    try:
        response = requests.get(f"{API_BASE_URL}/modelos", params=filtros)
        modelos = response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Erro ao conectar na API: {e}")
        modelos = []
    return render_template('index.html', modelos=modelos)

@app.route('/modelo/<int:id>')
def detalhes(id):
    try:
        response = requests.get(f"{API_BASE_URL}/modelo/{id}")
        trabalhos_resp = requests.get(f"{API_BASE_URL}/modelo/{id}/trabalhos")
        if response.status_code == 200:
            modelo = response.json()
            trabalhos = trabalhos_resp.json() if trabalhos_resp.status_code == 200 else []
            return render_template('detalhes.html', modelo=modelo, trabalhos=trabalhos)
    except Exception as e:
        print(f"Erro: {e}")
    return "Modelo não encontrada", 404

@app.route('/adicionar', methods=['POST'])
def adicionar():
    file = request.files.get('foto_arquivo')
    filename = "default.png"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    dados = {
        "nome": request.form.get("nome"),
        "idade": int(request.form.get("idade")),
        "peso": int(request.form.get("peso")),
        "altura": float(request.form.get("altura")),
        "cabelo": request.form.get("cabelo"),
        "pele": request.form.get("pele"),
        "olhos": request.form.get("olhos"),
        "busto": float(request.form.get("busto")),
        "cintura": float(request.form.get("cintura")),
        "quadril": float(request.form.get("quadril")),
        "evento_participado": request.form.get("evento_participado") or "",
        "foto_url": filename
    }
    requests.post(f"{API_BASE_URL}/modelos", json=dados)
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        response = requests.get(f"{API_BASE_URL}/modelo/{id}")
        if response.status_code == 200:
            return render_template('editar.html', modelo=response.json())
        return "Erro ao carregar", 404

    # Lógica de Upload e Limpeza de Foto Antiga
    file = request.files.get('foto_arquivo')
    foto_atual = request.form.get("foto_url") 
    filename = foto_atual 

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Deleta a foto antiga se não for a padrão e se for um arquivo diferente
        if foto_atual and foto_atual != "default.png" and foto_atual != filename:
            caminho_antigo = os.path.join(app.config['UPLOAD_FOLDER'], foto_atual)
            if os.path.exists(caminho_antigo):
                try:
                    os.remove(caminho_antigo)
                except Exception as e:
                    print(f"Erro ao deletar foto antiga: {e}")

    dados = {
        "nome": request.form.get("nome"),
        "idade": int(request.form.get("idade")),
        "peso": int(request.form.get("peso")),
        "altura": float(request.form.get("altura")),
        "cabelo": request.form.get("cabelo"),
        "pele": request.form.get("pele"),
        "olhos": request.form.get("olhos"),
        "busto": float(request.form.get("busto")),
        "cintura": float(request.form.get("cintura")),
        "quadril": float(request.form.get("quadril")),
        "evento_participado": request.form.get("evento_participado"),
        "foto_url": filename
    }
    requests.put(f"{API_BASE_URL}/modelos/{id}", json=dados)
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    try:
        resp = requests.get(f"{API_BASE_URL}/modelo/{id}")
        if resp.status_code == 200:
            foto = resp.json().get("foto_url")
            if foto and foto != "default.png":
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto)
                if os.path.exists(caminho):
                    os.remove(caminho)
    except:
        pass
    requests.delete(f"{API_BASE_URL}/modelos/{id}")
    return redirect(url_for('index'))

# --- ROTAS DE CLIENTES ---

@app.route('/clientes')
def listar_clientes_view():
    try:
        clientes = requests.get(f"{API_BASE_URL}/clientes").json()
    except:
        clientes = []
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/adicionar', methods=['POST'])
def adicionar_cliente():
    dados = {
        "nome": request.form.get("nome"),
        "telefone": request.form.get("telefone"),
        "email": request.form.get("email"),
        "cidade": request.form.get("cidade"),
        "estado": request.form.get("estado"),
        "pais": request.form.get("pais")
    }
    requests.post(f"{API_BASE_URL}/clientes", json=dados)
    return redirect(url_for('listar_clientes_view'))

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if request.method == 'GET':
        # Buscamos todos os clientes e filtramos o correto
        resp = requests.get(f"{API_BASE_URL}/clientes")
        clientes = resp.json()
        cliente = next((c for c in clientes if c['id'] == id), None)
        if cliente:
            return render_template('editar_cliente.html', cliente=cliente)
        return "Cliente não encontrado", 404

    dados = {
        "nome": request.form.get("nome"),
        "telefone": request.form.get("telefone"),
        "email": request.form.get("email"),
        "cidade": request.form.get("cidade"),
        "estado": request.form.get("estado"),
        "pais": request.form.get("pais")
    }
    requests.put(f"{API_BASE_URL}/clientes/{id}", json=dados)
    return redirect(url_for('listar_clientes_view'))

@app.route('/clientes/excluir/<int:id>')
def excluir_cliente_view(id):
    requests.delete(f"{API_BASE_URL}/clientes/{id}")
    return redirect(url_for('listar_clientes_view'))

# --- ROTAS DE TRABALHOS ---

@app.route('/trabalhos')
def listar_trabalhos_view():
    try:
        trabalhos = requests.get(f"{API_BASE_URL}/trabalhos").json()
        modelos = requests.get(f"{API_BASE_URL}/modelos").json()
        clientes = requests.get(f"{API_BASE_URL}/clientes").json()
    except:
        trabalhos, modelos, clientes = [], [], []
    return render_template('trabalhos.html', trabalhos=trabalhos, modelos=modelos, clientes=clientes)

@app.route('/trabalhos/adicionar', methods=['POST'])
def adicionar_trabalho():
    dados = {
        "modelo_id": int(request.form.get("modelo_id")),
        "cliente_id": int(request.form.get("cliente_id")),
        "data_inicio": request.form.get("data_inicio"),
        "data_fim": request.form.get("data_fim") or None,
        "cidade_trabalho": request.form.get("cidade_trabalho"),
        "estado_trabalho": request.form.get("estado_trabalho") or "N/A",
        "pais_trabalho": request.form.get("pais_trabalho") or "Brasil",
        "valor_trabalho": float(request.form.get("valor_trabalho"))
    }
    requests.post(f"{API_BASE_URL}/trabalhos", json=dados)
    return redirect(url_for('listar_trabalhos_view'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)

