CREATE DATABASE financegestor;
USE financegestor;

CREATE TABLE categorias (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE despesas(
	id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    categoria_id INT,
    descricao VARCHAR(255),
    valor DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

INSERT INTO categorias (nome) VALUES
('Alimentação'),
('Transporte'),
('Habitação'),
('Saúde');

CREATE TABLE IF NOT EXISTS orcamento (
	id INT PRIMARY KEY AUTO_INCREMENT,
    mes VARCHAR(7),
    valor FLOAT
);

CREATE TABLE poupancas (
	id INT AUTO_INCREMENT PRIMARY KEY,
    mes VARCHAR(7) UNIQUE,
    valor DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE metas (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	valor_alvo DECIMAL(10,2) NOT NULL,
	prazo DATE,
	criada_em DATE NOT NULL,
	concluida BOOLEAN DEFAULT FALSE,
	concluida_em DATE
)