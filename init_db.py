import pymysql
from sqlalchemy import create_engine, text

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'loja_vinil'

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

DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DATABASE_URI)

try:
    with engine.connect() as connection:
        with open("schema.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()
        for statement in sql_script.split(";"):
            if statement.strip():
                connection.execute(text(statement))
        print("Banco de dados configurado com sucesso!")
except Exception as e:
    print("Erro ao configurar o banco de dados:", e)

try:
    connection.close()
except NameError:
    pass
