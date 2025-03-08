from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.cliente import Cliente
from models.venda import Venda, ItensVenda
from datetime import datetime
from flask_login import login_required, current_user

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
@login_required
def listar_clientes():
    min_value = request.args.get('min_value', type=float)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Cliente.query
    
    if min_value:
        query = query.join(Venda).join(ItensVenda).filter(
            Venda.IDCliente == Cliente.IDCliente,
            (ItensVenda.Quantidade * ItensVenda.PrecoUnitario) > min_value
        )
    
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        query = query.filter(Venda.DataVenda >= start_date, Venda.DataVenda <= end_date)
    
    clientes = query.distinct().all()
    
    return render_template('clientes.html', clientes=clientes)

@clientes_bp.route('/cliente/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_cliente():
    if not current_user.Tipo == 'admin':
        flash('Você não tem permissão para adicionar clientes.', 'danger')
        return redirect(url_for('clientes.listar_clientes'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        
        novo_cliente = Cliente(Nome=nome, Email=email, Telefone=telefone, Endereco=endereco)

        try:
            db.session.add(novo_cliente)
            db.session.commit()
            flash('Cliente adicionado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar cliente: {str(e)}', 'error')

        return redirect(url_for('clientes.listar_clientes'))

    return render_template('adicionar_cliente.html')

@clientes_bp.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    if not current_user.Tipo == 'admin':
        flash('Você não tem permissão para editar clientes.', 'danger')
        return redirect(url_for('clientes.listar_clientes'))
    
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        cliente.Nome = request.form['nome']
        cliente.Email = request.form['email']
        cliente.Telefone = request.form['telefone']
        cliente.Endereco = request.form['endereco']

        try:
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cliente: {str(e)}', 'error')

        return redirect(url_for('clientes.listar_clientes'))
    
    return render_template('editar_cliente.html', cliente=cliente, editar=True)

@clientes_bp.route('/cliente/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_cliente(id):
    if not current_user.Tipo == 'admin':
        flash('Você não tem permissão para deletar clientes.', 'danger')
        return redirect(url_for('clientes.listar_clientes'))
    
    cliente = Cliente.query.get(id)
    
    if cliente:
        try:
            db.session.delete(cliente)
            db.session.commit()
            flash('Cliente deletado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar cliente: {str(e)}', 'error')
    else:
        flash('Cliente não encontrado!', 'error')
    
    return redirect(url_for('clientes.listar_clientes'))
