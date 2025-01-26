from . import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'Venda'

    IDVenda = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    DataVenda = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  
    ValorTotal = db.Column(db.Numeric(10, 2), nullable=False)  
    IDCliente = db.Column(db.Integer, db.ForeignKey('Cliente.IDCliente'), nullable=True)  

    itens_venda = db.relationship('ItensVenda', backref='venda', lazy=True)

    def __repr__(self):
        return f"<Venda {self.IDVenda} - {self.DataVenda} - R$ {self.ValorTotal}>"

class ItensVenda(db.Model):
    __tablename__ = 'ItensVenda'

    IDItensVenda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDVenda = db.Column(db.Integer, db.ForeignKey('Venda.IDVenda'), nullable=False)  # Adicionando chave estrangeira para Venda
    IDVinil = db.Column(db.Integer, db.ForeignKey('Vinil.IDVinil'), nullable=False)
    Quantidade = db.Column(db.Integer, nullable=False)
    PrecoUnitario = db.Column(db.Numeric(10, 2), nullable=False)

    vinil = db.relationship('Vinil', backref='itens_venda_rel', lazy=True)

    def __repr__(self):
        return f"<ItensVenda {self.IDItensVenda} - {self.Quantidade} - R$ {self.PrecoUnitario}>"
