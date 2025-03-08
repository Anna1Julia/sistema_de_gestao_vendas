from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user  
from models import db
from models.venda import Venda, ItensVenda
from models.cliente import Cliente
from models.vinil import Vinil

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/vendas', methods=['GET'])
@login_required
def listar_vendas():
    cliente_id = request.args.get('cliente_id')
    periodo = request.args.get('periodo')
    
    if periodo:
        today = datetime.today()
        if periodo == '7':
            data_inicio = today - timedelta(days=7)
        elif periodo == '30':
            data_inicio = today - timedelta(days=30)
        elif periodo == '60':
            data_inicio = today - timedelta(days=60)
        elif periodo == '90':
            data_inicio = today - timedelta(days=90)
        else:
            data_inicio = None
    else:
        data_inicio = None

    query = Venda.query

    if cliente_id:
        query = query.filter(Venda.cliente_id == cliente_id)

    if data_inicio:
        query = query.filter(Venda.DataVenda >= data_inicio)

    vendas = query.all()
    clientes = Cliente.query.all()

    return render_template('vendas.html', vendas=vendas, clientes=clientes)

@vendas_bp.route('/venda/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_venda():
    if not current_user.is_admin: 
        flash('Você não tem permissão para adicionar vendas.', 'error')
        return redirect(url_for('vendas.listar_vendas'))
    
    if request.method == 'POST':
        cliente_id = request.form.get('IDCliente')
        
        if not cliente_id:
            flash('Cliente não informado.', 'error')
            return redirect(url_for('vendas.adicionar_venda'))
        
        try:
            cliente_id = int(cliente_id)
        except ValueError:
            flash('ID do cliente inválido.', 'error')
            return redirect(url_for('vendas.adicionar_venda'))
        
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            flash('Cliente não encontrado.', 'error')
            return redirect(url_for('vendas.adicionar_venda'))
        
        vinis_selecionados = request.form.getlist('vinis[]')
        quantidades = request.form.getlist('quantidades[]')
        data_venda_str = request.form['data_venda']
        
        try:
            data_venda = datetime.strptime(data_venda_str, '%Y-%m-%d')
        except ValueError:
            flash('Data inválida. Por favor, insira uma data válida.', 'error')
            return redirect(url_for('vendas.adicionar_venda'))

        nova_venda = Venda(IDCliente=cliente_id, ValorTotal=0, DataVenda=data_venda)
        db.session.add(nova_venda)
        db.session.flush()

        valor_total = 0
        for vinil_id, quantidade in zip(vinis_selecionados, quantidades):
            vinil = Vinil.query.get(vinil_id)
            if vinil:
                try:
                    quantidade = int(quantidade)
                except ValueError:
                    flash(f"Quantidade inválida para o vinil '{vinil.Titulo}'.", 'error')
                    db.session.rollback()
                    return redirect(url_for('vendas.adicionar_venda'))
                
                if quantidade > vinil.Estoque:
                    flash(f"Quantidade solicitada para '{vinil.Titulo}' excede o estoque disponível!", 'error')
                    db.session.rollback()
                    return redirect(url_for('vendas.adicionar_venda'))
                
                preco_unitario = vinil.Preco or 0 
                if preco_unitario == 0:
                    flash(f"O vinil '{vinil.Titulo}' está com preço inválido!", 'error')
                    db.session.rollback()
                    return redirect(url_for('vendas.adicionar_venda'))

                item_venda = ItensVenda(
                    IDVenda=nova_venda.IDVenda,
                    IDVinil=vinil_id,
                    Quantidade=quantidade,
                    PrecoUnitario=preco_unitario
                )
                db.session.add(item_venda)
                valor_total += preco_unitario * quantidade
                vinil.Estoque -= quantidade

        nova_venda.ValorTotal = valor_total
        db.session.commit()

        flash('Venda adicionada com sucesso!', 'success')
        return redirect(url_for('vendas.listar_vendas'))

    vinis = Vinil.query.all()
    clientes = Cliente.query.all()
    return render_template('adicionar_venda.html', clientes=clientes, vinis=vinis)

@vendas_bp.route('/venda/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_venda(id):
    if not current_user.is_admin:
        flash('Você não tem permissão para deletar vendas.', 'error')
        return redirect(url_for('vendas.listar_vendas'))
    
    venda = Venda.query.get(id)
    if not venda:
        flash('Venda não encontrada!', 'error')
        return redirect(url_for('vendas.listar_vendas'))

    for item in venda.itens_venda:
        vinil = Vinil.query.get(item.IDVinil)
        if vinil:
            vinil.Estoque += item.Quantidade
        db.session.delete(item)

    db.session.delete(venda)
    db.session.commit()

    flash('Venda deletada com sucesso!', 'success')
    return redirect(url_for('vendas.listar_vendas'))
