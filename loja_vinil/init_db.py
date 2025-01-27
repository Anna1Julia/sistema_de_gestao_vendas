from sqlalchemy import create_engine

DATABASE_URI = 'mysql+pymysql://root:root@localhost/loja_vinil'

try:
    engine = create_engine(DATABASE_URI)
    connection = engine.connect()
    print("Conexão ao banco bem-sucedida!")
    connection.close()
except Exception as e:
    print("Erro ao conectar ao banco:", e)
