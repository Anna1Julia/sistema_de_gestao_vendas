from flask import Blueprint
from .vinis import vinis
from .clientes import clientes
from .vendas import vendas
from .generos import generos
from .pesquisa import pesquisa
from .main import main
from .usuario import usuario

vinis = Blueprint('vinis', __name__)
clientes = Blueprint('clientes', __name__)
vendas = Blueprint('vendas', __name__)
generos = Blueprint('generos', __name__)
pesquisa = Blueprint('pesquisa', __name__)
main = Blueprint('main', __name__)
usuario = Blueprint('usuario', __name__) 
