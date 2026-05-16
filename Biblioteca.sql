CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE modelos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT,
    peso INT,
    altura DECIMAL(5,2),
    cabelo VARCHAR(50),
    pele VARCHAR(50),
    olhos VARCHAR(50),
    busto DECIMAL(5,2),
    cintura DECIMAL(5,2),
    quadril DECIMAL(5,2),
    evento_participado TEXT,
    foto_url VARCHAR(255) DEFAULT 'default.png'
);

USE biblioteca;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    pais VARCHAR(50)
);

CREATE TABLE trabalhos (
    id_contrato INT AUTO_INCREMENT PRIMARY KEY,
    modelo_id INT NOT NULL,
    cliente_id INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    cidade_trabalho VARCHAR(100),
    estado_trabalho VARCHAR(50),
    pais_trabalho VARCHAR(50),
    valor_trabalho DECIMAL(10, 2),
    FOREIGN KEY (modelo_id) REFERENCES modelos(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);