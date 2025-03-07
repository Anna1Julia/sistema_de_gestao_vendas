from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.usuario import Usuario
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(Email=email).first()
        if usuario and check_password_hash(usuario.Senha, senha):
            login_user(usuario)
            flash('Você fez login com sucesso!', 'success')
            return redirect(url_for('main.index')) 
        else:
            flash('Email ou senha incorretos.', 'danger')
    return render_template('login.html')

@usuario_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'danger')
            return render_template('registro.html')
        
        usuario_existente = Usuario.query.filter_by(Email=email).first()
        if usuario_existente:
            flash('Este email já está cadastrado.', 'danger')
            return render_template('registro.html')
        
        novo_usuario = Usuario(Nome=nome, Email=email, Senha=generate_password_hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Sua conta foi criada com sucesso!', 'success')
        return redirect(url_for('usuario.login'))
    
    return render_template('registro.html')

@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você fez logout com sucesso.', 'success')
    return redirect(url_for('main.index'))
