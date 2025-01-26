from . import db

class Vinil(db.Model):
    __tablename__ = 'Vinil'

    IDVinil = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Titulo = db.Column(db.String(255), nullable=False)
    Artista = db.Column(db.String(255), nullable=False)
    AnoLancamento = db.Column(db.Integer)
    Preco = db.Column(db.Numeric(10, 2), nullable=False)
    Estoque = db.Column(db.Integer, nullable=False)
    IDGeneroMusical = db.Column(db.Integer, db.ForeignKey('GeneroMusical.IDGeneroMusical'), nullable=True)

    itens_venda = db.relationship('ItensVenda', backref='vinil_rel', lazy=True)

    def __repr__(self):
        return f"<Vinil {self.Titulo} - {self.Artista} - R$ {self.Preco}>"
