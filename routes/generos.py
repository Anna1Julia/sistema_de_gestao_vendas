from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.genero import GeneroMusical
from flask_login import login_required, current_user

generos_bp = Blueprint('generos', __name__)

@generos_bp.route('/generos')
@login_required
def listar_generos():
    generos = GeneroMusical.query.all()
    return render_template('generos.html', generos=generos)

@generos_bp.route('/genero/adicionar', methods=['POST'])
@login_required
def adicionar_genero():
    if not current_user.Tipo == 'admin':
        flash('Você não tem permissão para adicionar gêneros.', 'danger')
        return redirect(url_for('generos.listar_generos'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        novo_genero = GeneroMusical(Nome=nome)
        db.session.add(novo_genero)
        db.session.commit()
        flash('Gênero musical adicionado com sucesso!', 'success')
        return redirect(url_for('generos.listar_generos'))
    
@generos_bp.route('/genero/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_genero(id):
    if not current_user.Tipo == 'admin':
        flash('Você não tem permissão para editar gêneros.', 'danger')
        return redirect(url_for('generos.listar_generos'))
    
    genero = GeneroMusical.query.get_or_404(id)
    
    if request.method == 'POST':
        genero.Nome = request.form['nome']
        try:
            db.session.commit()
            flash('Gênero musical atualizado com sucesso!', 'success')
            return redirect(url_for('generos.listar_generos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar gênero: {str(e)}', 'error')
    
    return render_template('editar_genero.html', genero=genero)

@generos_bp.route('/genero/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_genero(id):
    if not current_user.Tipo == 'admin':
        flash('Você não tem permissão para excluir gêneros.', 'danger')
        return redirect(url_for('generos.listar_generos'))
    
    genero = GeneroMusical.query.get(id)
    if genero:
        try:
            db.session.delete(genero)
            db.session.commit()
            flash('Gênero excluído com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir gênero: {str(e)}', 'error')
    
    return redirect(url_for('generos.listar_generos'))

