from flask import Blueprint

vinis_bp = Blueprint('vinis', __name__)
clientes_bp = Blueprint('clientes', __name__)
vendas_bp = Blueprint('vendas', __name__)
generos_bp = Blueprint('generos', __name__)
pesquisa_bp = Blueprint('pesquisa', __name__)
main_bp = Blueprint('main', __name__)
usuario_bp = Blueprint('usuario', __name__)

from .vinis import *
from .clientes import *
from .vendas import *
from .generos import *
from .pesquisa import *
from .main import *
from .usuario import *