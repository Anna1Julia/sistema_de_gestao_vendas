from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db
from models.usuario import Usuario

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(Email=email).first()
        
        if usuario and check_password_hash(usuario.Senha, senha):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index')) 
            flash('Email ou senha incorretos!', 'error')

    return render_template('login.html')

@usuario_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash('As senhas não coincidem!', 'error')
            return redirect(url_for('usuario.register'))

        if Usuario.query.filter_by(Email=email).first():
            flash('Este email já está registrado!', 'error')
            return redirect(url_for('usuario.register'))

        senha_hash = generate_password_hash(senha, method='sha256')
        novo_usuario = Usuario(Nome=nome, Email=email, Senha=senha_hash)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('usuario.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar a conta: {str(e)}', 'error')

    return render_template('registro.html')

@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('index'))
