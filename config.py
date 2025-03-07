import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'root')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'mysql+pymysql://root:root@localhost/loja_vinil'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True  # Descomente se precisar ver as queries SQL no console
