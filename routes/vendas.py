from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.venda import Venda, ItensVenda
from models.vinil import Vinil
from models.cliente import Cliente
from models.log_venda import LogVenda

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/vendas', methods=['GET'])
@login_required
def listar_vendas():
    cliente_id = request.args.get('IDCliente') 
    periodo = request.args.get('periodo')
    
    vendas = Venda.query
    
    if cliente_id:
        vendas = vendas.filter_by(IDCliente=cliente_id)
    
    if periodo:
        try:
            periodo = int(periodo)
            data_limite = datetime.now() - timedelta(days=periodo)
            vendas = vendas.filter(Venda.DataVenda >= data_limite)
        except ValueError:
            pass
    
    vendas = vendas.all()
    
    clientes = Cliente.query.all()
    
    return render_template('vendas.html', vendas=vendas, clientes=clientes)

@vendas_bp.route('/venda/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_venda():
    if request.method == 'POST':
        cliente_id = request.form.get('IDCliente')
        data_venda = request.form.get('data_venda')

        if not cliente_id or not data_venda:
            flash("Preencha todos os campos obrigatórios", 'error')
            return redirect(url_for('vendas.adicionar_venda'))

        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            flash("Cliente não encontrado", 'error')
            return redirect(url_for('vendas.adicionar_venda'))

        vinis = request.form.getlist('vinis[]')
        quantidades = request.form.getlist('quantidades[]')

        vinis_filtrados = [v for v in vinis if v.strip()]
        quantidades_filtradas = [q for q in quantidades if q.strip()]

        if not vinis_filtrados or not quantidades_filtradas:
            flash("Selecione pelo menos um vinil válido", 'error')
            return redirect(url_for('vendas.adicionar_venda'))

        venda = Venda(IDCliente=cliente_id, DataVenda=data_venda, IDUsuario=current_user.IDUsuario)
        valor_total = 0

        for vinil_id, quantidade in zip(vinis_filtrados, quantidades_filtradas):
            try:
                vinil = Vinil.query.get(int(vinil_id))
                quantidade_int = int(quantidade)

                if not vinil:
                    flash(f"Vinil com ID {vinil_id} não encontrado", 'error')
                    db.session.rollback()
                    return redirect(url_for('vendas.adicionar_venda'))

                if vinil.Estoque < quantidade_int:
                    flash(f"Estoque insuficiente para {vinil.Titulo} (Estoque: {vinil.Estoque})", 'error')
                    db.session.rollback()
                    return redirect(url_for('vendas.adicionar_venda'))

                item_venda = ItensVenda(
                    IDVinil=vinil.IDVinil,
                    Quantidade=quantidade_int,
                    PrecoUnitario=vinil.Preco
                )
                venda.itens_venda.append(item_venda)

                vinil.Estoque -= quantidade_int
                db.session.add(vinil)

                valor_total += vinil.Preco * quantidade_int

            except ValueError:
                flash("Valores inválidos no formulário", 'error')
                db.session.rollback()
                return redirect(url_for('vendas.adicionar_venda'))

        venda.ValorTotal = valor_total
        db.session.add(venda)
        db.session.commit()

        log_venda = LogVenda(IDUsuario=current_user.IDUsuario, IDVenda=venda.IDVenda, Tipo='criação')
        db.session.add(log_venda)
        db.session.commit()

        flash("Venda registrada com sucesso!", 'success')
        return redirect(url_for('vendas.listar_vendas'))

    clientes = Cliente.query.all()
    vinis = Vinil.query.all()
    return render_template('adicionar_venda.html', clientes=clientes, vinis=vinis)

@vendas_bp.route('/venda/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_venda(id):
    venda = Venda.query.get(id)
    if not venda:
        flash('Venda não encontrada!', 'error')
        return redirect(url_for('vendas.listar_vendas'))

    clientes = Cliente.query.all()
    cliente = Cliente.query.get(venda.IDCliente)

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        vinis = request.form.getlist('vinis[]')
        quantidades = request.form.getlist('quantidades[]')

        if not cliente_id:
            flash("Selecione um cliente válido.", 'error')
            return redirect(url_for('vendas.editar_venda', id=id))

        if not vinis or not quantidades:
            flash("Selecione pelo menos um vinil válido.", 'error')
            return redirect(url_for('vendas.editar_venda', id=id))

        try:
            venda.IDCliente = int(cliente_id)

            for item in venda.itens_venda:
                vinil = Vinil.query.get(item.IDVinil)
                if vinil:
                    vinil.Estoque += item.Quantidade

            venda.itens_venda.clear()
            valor_total = 0

            for vinil_id, quantidade in zip(vinis, quantidades):
                vinil = Vinil.query.get(int(vinil_id))
                quantidade_int = int(quantidade)

                if not vinil:
                    flash(f"Vinil com ID {vinil_id} não encontrado.", 'error')
                    db.session.rollback()
                    return redirect(url_for('vendas.editar_venda', id=id))

                if vinil.Estoque < quantidade_int:
                    flash(f"Estoque insuficiente para {vinil.Titulo} (Estoque: {vinil.Estoque})", 'error')
                    db.session.rollback()
                    return redirect(url_for('vendas.editar_venda', id=id))

                item_venda = ItensVenda(
                    IDVenda=venda.IDVenda,
                    IDVinil=vinil.IDVinil,
                    Quantidade=quantidade_int,
                    PrecoUnitario=vinil.Preco
                )
                venda.itens_venda.append(item_venda)

                vinil.Estoque -= quantidade_int
                db.session.add(vinil)

                valor_total += vinil.Preco * quantidade_int

            venda.ValorTotal = valor_total
            db.session.commit()

            log_venda = LogVenda(IDUsuario=current_user.IDUsuario, IDVenda=venda.IDVenda, Tipo='edição')
            db.session.add(log_venda)
            db.session.commit()

            flash("Venda editada com sucesso!", 'success')
            return redirect(url_for('vendas.listar_vendas'))

        except ValueError:
            flash("Valores inválidos no formulário.", 'error')
            db.session.rollback()
            return redirect(url_for('vendas.editar_venda', id=id))

    itens_venda = [{'vinil': item.vinil, 'quantidade': item.Quantidade} for item in venda.itens_venda]
    vinis = Vinil.query.all()

    return render_template(
        'editar_venda.html', 
        venda=venda, 
        cliente=cliente, 
        clientes=clientes,
        itens_venda=itens_venda, 
        vinis=vinis
    )

@vendas_bp.route('/venda/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_venda(id):
    if not current_user.is_admin:
        flash('Você não tem permissão para deletar vendas.', 'error')
        return redirect(url_for('vendas.listar_vendas'))

    venda = Venda.query.filter_by(IDVenda=id).first_or_404()

    if not venda:
        flash('Venda não encontrada!', 'error')
        return redirect(url_for('vendas.listar_vendas'))

    try:
        if venda.IDVenda is None:
            flash('Erro: ID da venda não encontrado!', 'error')
            return redirect(url_for('vendas.listar_vendas'))

        log_venda = LogVenda(IDUsuario=current_user.IDUsuario, IDVenda=venda.IDVenda, Tipo='deletação')
        db.session.add(log_venda)

        for item in venda.itens_venda:
            vinil = Vinil.query.get(item.IDVinil)
            if vinil:
                vinil.Estoque += item.Quantidade

        db.session.delete(venda)
        db.session.commit()

        flash('Venda deletada com sucesso!', 'success')
        return redirect(url_for('vendas.listar_vendas'))
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao deletar a venda: {str(e)}', 'error')
        return redirect(url_for('vendas.listar_vendas'))

@vendas_bp.route('/log_vendas')
@login_required
def log_vendas():
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.index'))

    logs = LogVenda.query.order_by(LogVenda.DataHora.desc()).all()
    return render_template('log_vendas.html', logs=logs)