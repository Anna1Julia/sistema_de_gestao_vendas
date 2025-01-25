from . import db

class Genero(db.Model):
    __tablename__ = 'generos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    vinis = db.relationship('Vinil', backref='genero', lazy=True)

    def __repr__(self):
        return f"<Genero {self.nome}>"
