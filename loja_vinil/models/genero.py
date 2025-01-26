from . import db

class GeneroMusical(db.Model):
    __tablename__ = 'GeneroMusical'

    IDGeneroMusical = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(100), nullable=False)

    vinis = db.relationship('Vinil', backref='genero', lazy=True)

    def __repr__(self):
        return f"<GeneroMusical {self.Nome}>"
