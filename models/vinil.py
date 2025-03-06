from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import db

class Vinil(db.Model):
    __tablename__ = 'Vinil'

    IDVinil = Column(Integer, primary_key=True, autoincrement=True)
    Titulo = Column(String(100), nullable=False)
    Artista = Column(String(100), nullable=False)
    AnoLancamento = Column(Integer, nullable=True)
    Preco = Column(Float, nullable=True)
    Estoque = Column(Integer, nullable=False, default=0)
    IDGeneroMusical = Column(Integer, ForeignKey('GeneroMusical.IDGeneroMusical'), nullable=False)

    genero_musical = relationship('GeneroMusical', back_populates='vinis')

    def __repr__(self):
        return f"<Vinil {self.Titulo} - {self.Artista} - R$ {self.Preco}>"
