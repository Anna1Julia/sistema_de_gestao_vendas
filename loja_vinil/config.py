class Config:
    SECRET_KEY = 'root'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/loja_vinil'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True  # Descomente se precisar ver as queries SQL no console

