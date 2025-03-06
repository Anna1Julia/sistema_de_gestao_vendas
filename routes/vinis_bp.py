from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.vinil import Vinil
from models.genero import GeneroMusical

vinis_bp = Blueprint('vinis_bp_bp', __name__)

@vinis_bp.route('/vinis', methods=['GET'])
def listar_vinis():
    genero = request.args.get('genero', type=int)
    preco_min = request.args.get('preco_min', type=float)
    preco_max = request.args.get('preco_max', type=float)
    ordenar = request.args.get('ordenar', 'titulo')

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

    vinis = query.all()
    generos = GeneroMusical.query.all()
    return render_template('vinis.html', vinis=vinis, generos=generos)

@vinis_bp.route('/adicionar_vinil', methods=['GET', 'POST'])
def adicionar_vinil():
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

        return redirect(url_for('listar_vinis'))

    return render_template('adicionar_vinil.html', generos=generos)

@vinis_bp.route('/vinil/editar/<int:id>', methods=['GET', 'POST'])
def editar_vinil(id):
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

        return redirect(url_for('listar_vinis'))

    return render_template(
        'editar_vinil.html', 
        vinil=vinil, 
        generos=generos, 
        editar=True
    )

@vinis_bp.route('/deletar_vinil/<int:id>', methods=['POST'])
def deletar_vinil(id):
    vinil = Vinil.query.get_or_404(id)
    try:
        db.session.delete(vinil)
        db.session.commit()
        flash('Vinil deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar vinil: {str(e)}', 'error')
    return redirect(url_for('listar_vinis'))
