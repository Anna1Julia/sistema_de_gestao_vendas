from . import db

class Cliente(db.Model):
    __tablename__ = 'Cliente'

    IDCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Telefone = db.Column(db.String(20))
    Endereco = db.Column(db.Text)

    vendas = db.relationship('Venda', backref='cliente', lazy=True)

    def __repr__(self):
        return f"<Cliente {self.Nome}>"
