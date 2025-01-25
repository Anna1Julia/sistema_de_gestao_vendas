from . import db

class Vinil(db.Model):
    __tablename__ = 'vinis'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    genero_id = db.Column(db.Integer, db.ForeignKey('generos.id'), nullable=False)

    vendas = db.relationship('VendaVinil', backref='vinil', lazy=True)

    def __repr__(self):
        return f"<Vinil {self.titulo} - R$ {self.preco}>"
