from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.venda import ItensVenda, Venda
from models.vinil import Vinil
from models.genero import GeneroMusical
from datetime import datetime, timedelta

vinis_bp = Blueprint('vinis', __name__)

@vinis_bp.route('/vinis', methods=['GET'])
def listar_vinis():
    genero = request.args.get('genero', type=int)
    preco_min = request.args.get('preco_min', type=float)
    preco_max = request.args.get('preco_max', type=float)
    ordenar = request.args.get('ordenar', 'titulo')
    top_vendidos = request.args.get('top_vendidos', type=int)
    nao_vendidos = request.args.get('nao_vendidos', type=int)  # Novo filtro
    periodo = request.args.get('periodo', type=int)

    query = Vinil.query
    if genero:
        query = query.filter(Vinil.IDGeneroMusical == genero)
    if preco_min is not None:
        query = query.filter(Vinil.Preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Vinil.Preco <= preco_max)

    if ordenar == 'titulo':
        query = query.order_by(Vinil.Titulo)
    elif ordenar == 'preco':
        query = query.order_by(Vinil.Preco)
    elif ordenar == 'ano':
        query = query.order_by(Vinil.AnoLancamento)

    if periodo:
        hoje = datetime.today()
        inicio_periodo = hoje - timedelta(days=periodo)
        vendas = Venda.query.filter(Venda.DataVenda >= inicio_periodo).all()
    else:
        vendas = Venda.query.all()

    mensagem_vendas = "Não há vendas no período selecionado." if not vendas else None

    vinis_mais_vendidos = []
    if top_vendidos:
        vinis_vendidos_dict = {}

        for venda in vendas:
            for item in venda.itens_venda:
                vinil_id = item.IDVinil
                if vinil_id in vinis_vendidos_dict:
                    vinis_vendidos_dict[vinil_id] += item.Quantidade
                else:
                    vinis_vendidos_dict[vinil_id] = item.Quantidade

        top_10_vinis = sorted(vinis_vendidos_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        vinis_mais_vendidos = [Vinil.query.get(vinil_id) for vinil_id, _ in top_10_vinis]

    if nao_vendidos:
        vendidos = db.session.query(ItensVenda.IDVinil).distinct()
        query = query.filter(~Vinil.IDVinil.in_(vendidos))

    vinis = vinis_mais_vendidos if top_vendidos else query.all()
    generos = GeneroMusical.query.all()

    return render_template(
        'vinis.html',
        vinis=vinis,
        generos=generos,
        vinis_mais_vendidos=vinis_mais_vendidos,
        mensagem_vendas=mensagem_vendas
    )

@vinis_bp.route('/adicionar_vinil', methods=['GET', 'POST'])
@login_required
def adicionar_vinil():
    if not current_user.is_admin:
        flash('Você não tem permissão para adicionar vinis.', 'error')
        return redirect(url_for('vinis.listar_vinis'))  
    
    generos = GeneroMusical.query.all()
    if request.method == 'POST':
        titulo = request.form['titulo']
        artista = request.form['artista']
        ano_lancamento = request.form['ano_lancamento']
        preco = request.form['preco']
        estoque = request.form['estoque']
        genero_id = request.form['genero_id']

        novo_vinil = Vinil(
            Titulo=titulo,
            Artista=artista,
            AnoLancamento=ano_lancamento,
            Preco=preco,
            Estoque=estoque,
            IDGeneroMusical=genero_id
        )
        db.session.add(novo_vinil)
        try:
            db.session.commit()
            flash('Vinil adicionado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar vinil: {str(e)}', 'error')

        return redirect(url_for('vinis.listar_vinis'))

    return render_template('adicionar_vinil.html', generos=generos)

@vinis_bp.route('/vinil/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_vinil(id):
    if not current_user.is_admin:
        flash('Você não tem permissão para editar vinis.', 'error')
        return redirect(url_for('vinis.listar_vinis'))
    
    vinil = Vinil.query.get_or_404(id)
    generos = GeneroMusical.query.all()

    if request.method == 'POST':
        vinil.Titulo = request.form['titulo']
        vinil.Artista = request.form['artista']
        vinil.AnoLancamento = request.form['ano_lancamento']
        vinil.Preco = request.form['preco']
        vinil.Estoque = request.form['estoque']
        vinil.IDGeneroMusical = request.form['genero_id']

        try:
            db.session.commit()
            flash('Vinil atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar vinil: {str(e)}', 'error')

        return redirect(url_for('vinis.listar_vinis'))

    return render_template(
        'editar_vinil.html', 
        vinil=vinil, 
        generos=generos, 
        editar=True
    )

@vinis_bp.route('/deletar_vinil/<int:id>', methods=['POST'])
@login_required
def deletar_vinil(id):
    if not current_user.is_admin:  
        flash('Você não tem permissão para deletar vinis.', 'error')
        return redirect(url_for('vinis.listar_vinis'))  
    
    vinil = Vinil.query.get_or_404(id)
    try:
        db.session.delete(vinil)
        db.session.commit()
        flash('Vinil deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar vinil: {str(e)}', 'error')
    return redirect(url_for('vinis.listar_vinis'))
