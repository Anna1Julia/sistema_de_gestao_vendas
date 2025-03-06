CREATE DATABASE IF NOT EXISTS loja_vinil;
USE loja_vinil;

CREATE TABLE IF NOT EXISTS GeneroMusical (
    IDGeneroMusical INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Vinil (
    IDVinil INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Artista VARCHAR(255) NOT NULL,
    AnoLancamento YEAR,
    Preco DECIMAL(10, 2) NOT NULL,
    Estoque INT NOT NULL,
    IDGeneroMusical INT,
    FOREIGN KEY (IDGeneroMusical) REFERENCES GeneroMusical(IDGeneroMusical)
);

CREATE TABLE IF NOT EXISTS Cliente (
    IDCliente INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Telefone VARCHAR(20),
    Endereco TEXT
);

CREATE TABLE IF NOT EXISTS Venda (
    IDVenda INT AUTO_INCREMENT PRIMARY KEY,
    DataVenda DATETIME NOT NULL,
    ValorTotal DECIMAL(10, 2) NOT NULL,
    IDCliente INT,
    FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
);

CREATE TABLE IF NOT EXISTS ItensVenda (
    IDItensVenda INT AUTO_INCREMENT PRIMARY KEY,
    Quantidade INT NOT NULL,
    PrecoUnitario DECIMAL(10, 2) NOT NULL,
    IDVinil INT,
    IDVenda INT,
    FOREIGN KEY (IDVinil) REFERENCES Vinil(IDVinil),
    FOREIGN KEY (IDVenda) REFERENCES Venda(IDVenda)
);

CREATE TABLE IF NOT EXISTS Usuario (
    IDUsuario INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Senha VARCHAR(255) NOT NULL,
    Tipo ENUM('admin', 'comum') NOT NULL DEFAULT 'comum'
);

CREATE TABLE IF NOT EXISTS logs_vendas (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    operacao VARCHAR(10) NOT NULL,
    id_venda INT NOT NULL,
    id_cliente INT NOT NULL,
    usuario VARCHAR(255) NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_titulo_vinil ON Vinil(Titulo);
CREATE INDEX idx_nome_cliente ON Cliente(Nome);
CREATE INDEX idx_data_venda ON Venda(DataVenda);

DELIMITER //
CREATE TRIGGER verificar_estoque
BEFORE INSERT ON ItensVenda
FOR EACH ROW
BEGIN
    DECLARE estoque_atual INT;
    SELECT Estoque INTO estoque_atual FROM Vinil WHERE IDVinil = NEW.IDVinil;
    IF estoque_atual < NEW.Quantidade THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Não há estoque suficiente!';
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER log_vendas
AFTER INSERT ON Venda
FOR EACH ROW
BEGIN
    INSERT INTO logs_vendas (operacao, id_venda, id_cliente, usuario)
    VALUES ('INSERT', NEW.IDVenda, NEW.IDCliente, 'Sistema');
END;
//
DELIMITER ;

INSERT INTO Usuario (Nome, Email, Senha, Tipo) 
VALUES ('Admin', 'admin@email.com', SHA2('senha123', 256), 'admin')
ON DUPLICATE KEY UPDATE Email=Email;
