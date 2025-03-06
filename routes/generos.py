from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.genero import GeneroMusical

generos = Blueprint('generos', __name__)

@generos.route('/generos')
def listar_generos():
    generos = GeneroMusical.query.all()
    return render_template('generos.html', generos=generos)

@generos.route('/genero/adicionar', methods=['POST'])
def adicionar_genero():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_genero = GeneroMusical(Nome=nome)
        db.session.add(novo_genero)
        db.session.commit()
        flash('Gênero musical adicionado com sucesso!', 'success')
        return redirect(url_for('listar_generos'))

@generos.route('/genero/deletar/<int:id>', methods=['POST'])
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
    return redirect(url_for('listar_generos'))

