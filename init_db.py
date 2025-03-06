import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text

# Configurações de conexão
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'loja_vinil'

# Conectando diretamente via pymysql para criar o banco de dados, caso não exista
try:
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        connection.commit()
    print(f"Banco de dados '{DB_NAME}' criado ou já existente!")
except Exception as e:
    print("Erro ao criar o banco de dados:", e)
finally:
    connection.close()

# Agora conectando ao banco de dados 'loja_vinil' via SQLAlchemy
DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DATABASE_URI)

# Conectando ao banco de dados 'loja_vinil'
try:
    connection = engine.connect()
    print("Conexão ao banco bem-sucedida!")
except Exception as e:
    print("Erro ao conectar ao banco:", e)

# Script de criação das tabelas
create_tables_sql = [
    '''
    CREATE TABLE IF NOT EXISTS GeneroMusical (
        IDGeneroMusical INT AUTO_INCREMENT PRIMARY KEY,
        Nome VARCHAR(100) NOT NULL
    );
    ''',
    '''
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
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Cliente (
        IDCliente INT AUTO_INCREMENT PRIMARY KEY,
        Nome VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL UNIQUE,
        Telefone VARCHAR(20),
        Endereco TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Venda (
        IDVenda INT AUTO_INCREMENT PRIMARY KEY,
        DataVenda DATETIME NOT NULL,
        ValorTotal DECIMAL(10, 2) NOT NULL,
        IDCliente INT,
        FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS ItensVenda (
        IDItensVenda INT AUTO_INCREMENT PRIMARY KEY,
        Quantidade INT NOT NULL,
        PrecoUnitario DECIMAL(10, 2) NOT NULL,
        IDVinil INT,
        IDVenda INT,
        FOREIGN KEY (IDVinil) REFERENCES Vinil(IDVinil),
        FOREIGN KEY (IDVenda) REFERENCES Venda(IDVenda)
    );
    '''
]

# Executando a criação das tabelas
try:
    with engine.connect() as connection:
        for sql in create_tables_sql:
            connection.execute(text(sql))
        print("Tabelas criadas com sucesso!")
except Exception as e:
    print("Erro ao criar o schema:", e)

# Script para criação dos índices
create_indexes_sql = [
    'CREATE INDEX idx_titulo_vinil ON Vinil(Titulo);',
    'CREATE INDEX idx_nome_cliente ON Cliente(Nome);',
    'CREATE INDEX idx_data_venda ON Venda(DataVenda);'
]

# Executando a criação dos índices
try:
    with engine.connect() as connection:
        for sql in create_indexes_sql:
            connection.execute(text(sql))
        print("Índices criados com sucesso!")
except Exception as e:
    print("Erro ao criar os índices:", e)

# Fechar a conexão com o banco
try:
    connection.close()
except NameError:
    pass  # Se a conexão não foi estabelecida, ignora o erro
