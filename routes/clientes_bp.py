from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.cliente import Cliente
from models.venda import Venda, ItensVenda
from datetime import datetime

clientes_bp = Blueprint('clientes', __name__)

def validar_data(data_str):
    try:
        return datetime.strptime(data_str, '%Y-%m-%d')
    except ValueError:
        return None

@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    min_value = request.args.get('min_value', type=float)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Cliente.query
    
    if min_value:
        query = query.join(Venda, Venda.IDCliente == Cliente.IDCliente)\
                     .join(ItensVenda, ItensVenda.IDVenda == Venda.IDVenda)\
                     .filter((ItensVenda.Quantidade * ItensVenda.PrecoUnitario) > min_value)
    
    if start_date and end_date:
        start_date = validar_data(start_date)
        end_date = validar_data(end_date)
        
        if not start_date or not end_date:
            flash('Formato de data inválido. Use o formato AAAA-MM-DD.', 'error')
            return redirect(url_for('clientes.listar_clientes'))
        
        query = query.filter(Venda.DataVenda >= start_date, Venda.DataVenda <= end_date)
    
    clientes = query.all()
    
    return render_template('clientes.html', clientes=clientes)

@clientes_bp.route('/cliente/adicionar', methods=['GET', 'POST'])
def adicionar_cliente():
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
def editar_cliente(id):
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
def deletar_cliente(id):
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
