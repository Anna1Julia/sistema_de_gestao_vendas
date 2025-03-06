from flask import Blueprint, render_template, request
from models.venda import Venda
from models.vinil import Vinil
from models.cliente import Cliente

pesquisa_bp = Blueprint('pesquisa', __name__)

@pesquisa_bp.route('/pesquisar', methods=['GET'])
def pesquisar():
    search_query = request.args.get('search', '')

    resultados = {
        'vendas': [],
        'vinis': [],
        'clientes': []
    }

    if search_query:
        resultados['vendas'] = Venda.query.filter(
            Venda.DataVenda.like(f"%{search_query}%")
        ).all()

        resultados['vinis'] = Vinil.query.filter(
            Vinil.Titulo.like(f"%{search_query}%") |
            Vinil.Artista.like(f"%{search_query}%")
        ).all()

        resultados['clientes'] = Cliente.query.filter(
            Cliente.Nome.like(f"%{search_query}%") |
            Cliente.Email.like(f"%{search_query}%")
        ).all()

    return render_template('pesquisar.html', resultados=resultados, search=search_query)
