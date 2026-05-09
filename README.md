Phas Models

O Phas Models é um sistema completo de gestão para agências de modelos. Ele permite o cadastro de modelos com imagem, gestão de clientes e registro de contratos, tudo isso sob uma interface moderna e responsiva.
Tecnologias Utilizadas: 
Backend API: FastAPI (Python)
Frontend/Server: Flask (Python)
Banco de Dados: MySQLInterface
Integração: Requests (Comunicação entre Flask e FastAPI)
Estrutura do Projeto
├── app_flask.py
├── api_fast.py
├── static/
│   ├── fundo-phas.jpg
│   ├── logo-phas.png
│   └── uploads/
├── templates/
│   ├── index.html
│   ├── detalhes.html
│   ├── editar.html
│   ├── clientes.html
│   ├── editar_cliente.html
│   └── trabalhos.html
└── README.md

Requisitos:
Python 3.8
MySQL
Banco de Dados: crie as tabelas necessárias no seu MySQL (Baseado nos Schemas do projeto):CREATE DATABASE biblioteca; USE biblioteca;
- Tabela de Modelos, Clientes e Trabalhos

Instalação de Dependências: pip install flask fastapi uvicorn mysql-connector-python requests pydantic
Execução: para rodar o sistema, você precisa iniciar dois serviços simultaneamente:Inicie a API (Backend):python api_fast.py e inicie o Flask (Frontend):python app_flask.py .
O sistema estará disponível em http://localhost:5000

Funcionalidades
Modelos: Cadastro completo com medidas, características físicas e upload de foto.
Filtros Inteligentes: Busca de modelos por nome, cor de cabelo, pele, etc.
Clientes: Cadastro e edição de clientes contratantes.
Controle de Trabalhos: Registro de contratos vinculando modelos, clientes e valores.

Desenvolvido para Phas Models.
