from . import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    
    IDUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Senha = db.Column(db.String(255), nullable=False)
    Tipo = db.Column(db.String(10), nullable=False, default='comum')

    def get_id(self):
        return self.IDUsuario
