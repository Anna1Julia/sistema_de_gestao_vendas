from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import db

class GeneroMusical(db.Model):
    __tablename__ = 'GeneroMusical'

    IDGeneroMusical = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(100), nullable=False, unique=True)

    vinis = relationship('Vinil', back_populates='genero_musical', lazy='dynamic')

    def __repr__(self):
        return f"<GeneroMusical {self.Nome}>"
