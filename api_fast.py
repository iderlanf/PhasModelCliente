from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
import mysql.connector
from typing import List, Optional, Any
from datetime import date

app = FastAPI(title="API de Gestão Phas Models")

# Configuração do Banco de Dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "0510",
    "database": "biblioteca"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- SCHEMAS (MODELOS) ---

class ModeloSchema(BaseModel):
    nome: str
    idade: int
    peso: int
    altura: float
    cabelo: str
    pele: str
    olhos: str
    busto: float
    cintura: float
    quadril: float
    evento_participado: str
    foto_url: Optional[str] = "default.png"

class ModeloDB(ModeloSchema):
    id: int
    @field_validator('altura', 'busto', 'cintura', 'quadril', mode='before')
    @classmethod
    def convert_decimal(cls, v: Any) -> float:
        return float(v) if v is not None else 0.0

# --- SCHEMAS (CLIENTES) ---

class ClienteSchema(BaseModel):
    nome: str
    telefone: Optional[str]
    email: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    pais: Optional[str]

class ClienteDB(ClienteSchema):
    id: int

# --- SCHEMAS (TRABALHOS) ---

class TrabalhoSchema(BaseModel):
    modelo_id: int
    cliente_id: int
    data_inicio: date
    data_fim: Optional[date]
    cidade_trabalho: str
    estado_trabalho: str
    pais_trabalho: str
    valor_trabalho: float

class TrabalhoDB(TrabalhoSchema):
    id_contrato: int

# --- ROTAS DE MODELOS ---

@app.get("/modelos", response_model=List[ModeloDB])
def listar_modelos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM modelos")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.post("/modelos", status_code=status.HTTP_201_CREATED)
def criar_modelo(modelo: ModeloSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO modelos (nome, idade, peso, altura, cabelo, pele, olhos, busto, cintura, quadril, evento_participado, foto_url) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (modelo.nome, modelo.idade, modelo.peso, modelo.altura, modelo.cabelo, modelo.pele, modelo.olhos, modelo.busto, modelo.cintura, modelo.quadril, modelo.evento_participado, modelo.foto_url)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return {"message": "Modelo cadastrada com sucesso"}

@app.get("/modelo/{id}", response_model=ModeloDB)
def buscar_modelo(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM modelos WHERE id = %s", (id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Modelo não encontrada")
    return item

# --- ROTAS DE CLIENTES ---

@app.get("/clientes", response_model=List[ClienteDB])
def listar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.post("/clientes", status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO clientes (nome, telefone, email, cidade, estado, pais) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (cliente.nome, cliente.telefone, cliente.email, cliente.cidade, cliente.estado, cliente.pais))
    conn.commit()
    conn.close()
    return {"message": "Cliente cadastrado com sucesso"}

# --- ROTAS DE TRABALHOS (CONTRATOS) ---

@app.get("/trabalhos", response_model=List[TrabalhoDB])
def listar_trabalhos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trabalhos")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.post("/trabalhos", status_code=status.HTTP_201_CREATED)
def criar_trabalho(trabalho: TrabalhoSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO trabalhos (modelo_id, cliente_id, data_inicio, data_fim, cidade_trabalho, estado_trabalho, pais_trabalho, valor_trabalho) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (trabalho.modelo_id, trabalho.cliente_id, trabalho.data_inicio, trabalho.data_fim, trabalho.cidade_trabalho, trabalho.estado_trabalho, trabalho.pais_trabalho, trabalho.valor_trabalho)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return {"message": "Trabalho registrado com sucesso"}

# Rota para ver trabalhos de uma modelo específica
@app.get("/modelo/{id}/trabalhos")
def ver_trabalhos_modelo(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT t.*, c.nome as nome_cliente 
        FROM trabalhos t 
        JOIN clientes c ON t.cliente_id = c.id 
        WHERE t.modelo_id = %s
    """
    cursor.execute(query, (id,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
