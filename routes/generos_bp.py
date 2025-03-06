from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.genero import GeneroMusical

generos_bp = Blueprint('generos', __name__)

@generos_bp.route('/generos')
def listar_generos():
    generos = GeneroMusical.query.all()
    return render_template('generos.html', generos=generos)

@generos_bp.route('/genero/adicionar', methods=['POST'])
def adicionar_genero():
    if request.method == 'POST':
        nome = request.form['nome']
        if not nome:
            flash('O nome do gênero musical não pode ser vazio!', 'error')
            return redirect(url_for('generos.listar_generos'))
        
        novo_genero = GeneroMusical(Nome=nome)
        try:
            db.session.add(novo_genero)
            db.session.commit()
            flash('Gênero musical adicionado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar gênero musical: {str(e)}', 'error')
        
        return redirect(url_for('generos.listar_generos'))

@generos_bp.route('/genero/deletar/<int:id>', methods=['POST'])
def deletar_genero(id):
    genero = GeneroMusical.query.get(id)
    if genero:
        try:
            db.session.delete(genero)
            db.session.commit()
            flash('Gênero excluído com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir gênero: {str(e)}', 'error')
    else:
        flash('Gênero não encontrado!', 'error')
    return redirect(url_for('generos.listar_generos'))
