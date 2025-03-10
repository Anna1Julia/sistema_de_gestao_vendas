from . import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'Venda'

    IDVenda = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    DataVenda = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  
    ValorTotal = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  
    IDCliente = db.Column(db.Integer, db.ForeignKey('Cliente.IDCliente'), nullable=True)  

    itens_venda = db.relationship('ItensVenda', backref='venda', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Venda {self.IDVenda} - {self.DataVenda} - R$ {self.ValorTotal}>"

    def atualizar_valor_total(self):
        self.ValorTotal = sum(item.Quantidade * item.PrecoUnitario for item in self.itens_venda)
        db.session.commit()

class ItensVenda(db.Model):
    __tablename__ = 'ItensVenda'

    IDItensVenda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDVenda = db.Column(db.Integer, db.ForeignKey('Venda.IDVenda'), nullable=False)
    IDVinil = db.Column(db.Integer, db.ForeignKey('Vinil.IDVinil'), nullable=False)
    Quantidade = db.Column(db.Integer, nullable=False)
    PrecoUnitario = db.Column(db.Numeric(10, 2), nullable=False)

    vinil = db.relationship('Vinil', backref='itens_venda_rel', lazy=True)

    def __repr__(self):
        return f"<ItensVenda {self.IDItensVenda} - {self.Quantidade} - R$ {self.PrecoUnitario}>"
