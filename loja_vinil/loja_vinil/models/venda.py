from . import db
from datetime import datetime
class VendaVinil(db.Model):
    __tablename__ = 'venda_vinil'

    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), primary_key=True)
    vinil_id = db.Column(db.Integer, db.ForeignKey('vinis.id'), primary_key=True)

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    vinis = db.relationship('VendaVinil', backref='venda', lazy=True)

    def __repr__(self):
        return f"<Venda {self.id} - Cliente {self.cliente.nome}>"
