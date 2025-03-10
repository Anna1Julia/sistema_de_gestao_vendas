from . import db
from datetime import datetime

class LogAcesso(db.Model):
    __tablename__ = 'LogAcesso'

    IDLog = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.IDUsuario'), nullable=True)
    Email = db.Column(db.String(255), nullable=False)
    DataHora = db.Column(db.DateTime, default=datetime.utcnow)
    Tipo = db.Column(db.String(20), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('logs', lazy=True))
