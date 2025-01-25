from . import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    telefone = db.Column(db.String(15), nullable=True)

    vendas = db.relationship('Venda', backref='cliente', lazy=True)

    def __repr__(self):
        return f"<Cliente {self.nome}>"
