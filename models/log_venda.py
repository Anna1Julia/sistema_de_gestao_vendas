from . import db
from datetime import datetime

class LogVenda(db.Model):
    __tablename__ = 'LogVenda'

    IDLogVenda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.IDUsuario'), nullable=False)  # Relacionamento com o usuário
    IDVenda = db.Column(db.Integer, db.ForeignKey('Venda.IDVenda'), nullable=False)  # Relacionamento com a venda
    DataHora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Data e hora do log
    Tipo = db.Column(db.String(20), nullable=False)  # Tipo de log: 'criação', 'atualização', etc.

    usuario = db.relationship('Usuario', backref='logs_venda', lazy=True)
    venda = db.relationship('Venda', backref='logs_venda', lazy=True)

    def __repr__(self):
        return f"<LogVenda {self.IDLogVenda} - {self.DataHora} - {self.Tipo}>"
