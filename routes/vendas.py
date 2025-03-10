from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.venda import Venda, ItensVenda
from models.vinil import Vinil
from models.cliente import Cliente
from models.log_venda import LogVenda

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/vendas')
@login_required
def listar_vendas():
    vendas = Venda.query.all()
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

        venda = Venda(IDCliente=cliente_id, DataVenda=data_venda)
        valor_total = 0

        vinis = request.form.getlist('vinis[]')
        quantidades = request.form.getlist('quantidades[]')

        if len(vinis) != len(quantidades) or len(vinis) == 0:
            flash("Selecione pelo menos um vinil com quantidade válida", 'error')
            return redirect(url_for('vendas.adicionar_venda'))

        for vinil_id, quantidade in zip(vinis, quantidades):
            if not vinil_id or not quantidade:
                flash("Preencha todos os campos de vinil e quantidade", 'error')
                return redirect(url_for('vendas.adicionar_venda'))

            try:
                vinil = Vinil.query.get(int(vinil_id))
                quantidade_int = int(quantidade)

                if vinil is None:
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

@vendas_bp.route('/venda/editar/<int:id>', methods=['POST'])
@login_required
def editar_venda(id):
    venda = Venda.query.get(id)
    if not venda:
        flash('Venda não encontrada!', 'error')
        return redirect(url_for('vendas.listar_vendas'))

    for item in request.form.getlist('itens'):
        item_existente = ItensVenda.query.filter_by(IDVenda=venda.IDVenda, IDVinil=item['IDVinil']).first()
        if item_existente:
            item_existente.Quantidade += item['quantidade']
        else:
            vinil = Vinil.query.get(item['IDVinil'])
            novo_item = ItensVenda(
                IDVinil=vinil.IDVinil,
                Quantidade=item['quantidade'],
                PrecoUnitario=vinil.Preco
            )
            venda.itens_venda.append(novo_item)

    venda.atualizar_valor_total()

    db.session.commit()

    log_venda = LogVenda(IDUsuario=current_user.IDUsuario, IDVenda=venda.IDVenda, Tipo='edição')
    db.session.add(log_venda)
    db.session.commit()

    flash('Venda editada com sucesso!', 'success')
    return redirect(url_for('vendas.listar_vendas'))

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

    log_venda = LogVenda(IDUsuario=current_user.IDUsuario, IDVenda=venda.IDVenda, Tipo='deletação')
    db.session.add(log_venda)
    db.session.commit()

    flash('Venda deletada com sucesso!', 'success')
    return redirect(url_for('vendas.listar_vendas'))

@vendas_bp.route('/log_vendas')
@login_required
def log_vendas():
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.index'))

    logs = LogVenda.query.order_by(LogVenda.DataHora.desc()).all()
    return render_template('log_vendas.html', logs=logs)