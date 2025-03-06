from flask import Flask, render_template, request, redirect, url_for, flash
from models import db
from models.genero import GeneroMusical
from models.vinil import Vinil
from models.cliente import Cliente
from models.venda import Venda, ItensVenda
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

app.secret_key = 'root'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vinis', methods=['GET'])
def listar_vinis():
    genero = request.args.get('genero', type=int)
    preco_min = request.args.get('preco_min', type=float)
    preco_max = request.args.get('preco_max', type=float)
    ordenar = request.args.get('ordenar', 'titulo')

    query = Vinil.query
    if genero:
        query = query.filter(Vinil.IDGeneroMusical == genero)
    if preco_min is not None:
        query = query.filter(Vinil.Preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Vinil.Preco <= preco_max)

    if ordenar == 'titulo':
        query = query.order_by(Vinil.Titulo)
    elif ordenar == 'preco':
        query = query.order_by(Vinil.Preco)
    elif ordenar == 'ano':
        query = query.order_by(Vinil.AnoLancamento)

    vinis = query.all()
    generos = GeneroMusical.query.all()
    return render_template('vinis.html', vinis=vinis, generos=generos)

@app.route('/adicionar_vinil', methods=['GET', 'POST'])
def adicionar_vinil():
    generos = GeneroMusical.query.all()
    if request.method == 'POST':
        titulo = request.form['titulo']
        artista = request.form['artista']
        ano_lancamento = request.form['ano_lancamento']
        preco = request.form['preco']
        estoque = request.form['estoque']
        genero_id = request.form['genero_id']

        novo_vinil = Vinil(
            Titulo=titulo,
            Artista=artista,
            AnoLancamento=ano_lancamento,
            Preco=preco,
            Estoque=estoque,
            IDGeneroMusical=genero_id
        )
        db.session.add(novo_vinil)
        try:
            db.session.commit()
            flash('Vinil adicionado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar vinil: {str(e)}', 'error')

        return redirect(url_for('listar_vinis'))

    return render_template('adicionar_vinil.html', generos=generos)

@app.route('/vinil/editar/<int:id>', methods=['GET', 'POST'])
def editar_vinil(id):
    vinil = Vinil.query.get_or_404(id)
    generos = GeneroMusical.query.all()

    if request.method == 'POST':
        vinil.Titulo = request.form['titulo']
        vinil.Artista = request.form['artista']
        vinil.AnoLancamento = request.form['ano_lancamento']
        vinil.Preco = request.form['preco']
        vinil.Estoque = request.form['estoque']
        vinil.IDGeneroMusical = request.form['genero_id']

        try:
            db.session.commit()
            flash('Vinil atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar vinil: {str(e)}', 'error')

        return redirect(url_for('listar_vinis'))

    return render_template(
        'editar_vinil.html', 
        vinil=vinil, 
        generos=generos, 
        editar=True
    )

@app.route('/deletar_vinil/<int:id>', methods=['POST'])
def deletar_vinil(id):
    vinil = Vinil.query.get_or_404(id)
    try:
        db.session.delete(vinil)
        db.session.commit()
        flash('Vinil deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar vinil: {str(e)}', 'error')
    return redirect(url_for('listar_vinis'))

@app.route('/clientes', methods=['GET'])
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

@app.route('/cliente/adicionar', methods=['GET', 'POST'])
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

        return redirect(url_for('listar_clientes'))

    return render_template('adicionar_cliente.html')

@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
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

        return redirect(url_for('listar_clientes'))

    return render_template(
        'editar_cliente.html', 
        cliente=cliente, 
        editar=True  
    )

@app.route('/cliente/deletar/<int:id>', methods=['POST'])
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
    return redirect(url_for('listar_clientes'))

@app.route('/vendas', methods=['GET'])
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

@app.route('/venda/adicionar', methods=['GET', 'POST'])
def adicionar_venda():
    if request.method == 'POST':
        cliente_id = request.form.get('IDCliente')
        
        if not cliente_id:
            flash('Cliente não informado.', 'error')
            return redirect(url_for('adicionar_venda'))
        
        try:
            cliente_id = int(cliente_id)
        except ValueError:
            flash('ID do cliente inválido.', 'error')
            return redirect(url_for('adicionar_venda'))
        
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            flash('Cliente não encontrado.', 'error')
            return redirect(url_for('adicionar_venda'))
        
        vinis_selecionados = request.form.getlist('vinis[]')
        quantidades = request.form.getlist('quantidades[]')
        data_venda_str = request.form['data_venda']
        
        try:
            data_venda = datetime.strptime(data_venda_str, '%Y-%m-%d')
        except ValueError:
            flash('Data inválida. Por favor, insira uma data válida.', 'error')
            return redirect(url_for('adicionar_venda'))

        nova_venda = Venda(IDCliente=cliente_id, ValorTotal=0, DataVenda=data_venda)
        db.session.add(nova_venda)
        db.session.flush()  # Para garantir que IDVenda esteja disponível

        valor_total = 0
        for vinil_id, quantidade in zip(vinis_selecionados, quantidades):
            vinil = Vinil.query.get(vinil_id)
            if vinil:
                try:
                    quantidade = int(quantidade)
                except ValueError:
                    flash(f"Quantidade inválida para o vinil '{vinil.Titulo}'.", 'error')
                    db.session.rollback()
                    return redirect(url_for('adicionar_venda'))
                
                if quantidade > vinil.Estoque:
                    flash(f"Quantidade solicitada para '{vinil.Titulo}' excede o estoque disponível!", 'error')
                    db.session.rollback()
                    return redirect(url_for('adicionar_venda'))
                
                preco_unitario = vinil.Preco or 0 
                if preco_unitario == 0:
                    flash(f"O vinil '{vinil.Titulo}' está com preço inválido!", 'error')
                    db.session.rollback()
                    return redirect(url_for('adicionar_venda'))

                item_venda = ItensVenda(
                    IDVenda=nova_venda.IDVenda,
                    IDVinil=vinil_id,
                    Quantidade=quantidade,
                    PrecoUnitario=preco_unitario
                )
                db.session.add(item_venda)
                valor_total += preco_unitario * quantidade
                vinil.Estoque -= quantidade  # Atualiza o estoque do vinil

        nova_venda.ValorTotal = valor_total
        db.session.commit()

        flash('Venda adicionada com sucesso!', 'success')
        return redirect(url_for('listar_vendas'))

    vinis = Vinil.query.all()
    clientes = Cliente.query.all()
    return render_template('adicionar_venda.html', clientes=clientes, vinis=vinis)

@app.route('/venda/editar/<int:id>', methods=['GET', 'POST'])
def editar_venda(id):
    venda = Venda.query.get_or_404(id) 
    vinis = Vinil.query.all() 
    clientes = Cliente.query.all() 

    if request.method == 'POST':
        venda.IDCliente = request.form['cliente_id']
        
        vinis_selecionados = request.form.getlist('vinis[]')
        quantidades = request.form.getlist('quantidades[]')
        
        # Remover os itens da venda para atualização
        ItensVenda.query.filter_by(IDVenda=venda.IDVenda).delete()

        valor_total = 0
        for vinil_id, quantidade in zip(vinis_selecionados, quantidades):
            vinil = Vinil.query.get(vinil_id)
            if vinil:
                try:
                    quantidade = int(quantidade)
                except ValueError:
                    flash(f"Quantidade inválida para o vinil '{vinil.Titulo}'.", 'error')
                    db.session.rollback()
                    return redirect(url_for('editar_venda', id=id))
                
                if quantidade > vinil.Estoque:
                    flash(f"Quantidade solicitada para '{vinil.Titulo}' excede o estoque disponível!", 'error')
                    return redirect(url_for('editar_venda', id=id))
                
                preco_unitario = vinil.Preco or 0 
                if preco_unitario == 0:
                    flash(f"O vinil '{vinil.Titulo}' está com preço inválido!", 'error')
                    return redirect(url_for('editar_venda', id=id))

                item_venda = ItensVenda(
                    IDVenda=venda.IDVenda,
                    IDVinil=vinil_id,
                    Quantidade=quantidade,
                    PrecoUnitario=preco_unitario
                )
                db.session.add(item_venda)
                valor_total += preco_unitario * quantidade
                vinil.Estoque -= quantidade  # Atualiza o estoque do vinil

        venda.ValorTotal = valor_total
        db.session.commit()

        flash('Venda atualizada com sucesso!', 'success')
        return redirect(url_for('listar_vendas'))

    return render_template('editar_venda.html', venda=venda, vinis=vinis, clientes=clientes)

@app.route('/venda/deletar/<int:id>', methods=['POST'])
def deletar_venda(id):
    venda = Venda.query.get(id)
    if not venda:
        flash('Venda não encontrada!', 'error')
        return redirect(url_for('listar_vendas'))

    for item in venda.itens_venda:
        vinil = Vinil.query.get(item.IDVinil)
        if vinil:
            vinil.Estoque += item.Quantidade
        db.session.delete(item)

    db.session.delete(venda)
    db.session.commit()

    flash('Venda deletada com sucesso!', 'success')
    return redirect(url_for('listar_vendas'))

@app.route('/generos')
def listar_generos():
    generos = GeneroMusical.query.all()
    return render_template('generos.html', generos=generos)

@app.route('/genero/adicionar', methods=['POST'])
def adicionar_genero():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_genero = GeneroMusical(Nome=nome)
        db.session.add(novo_genero)
        db.session.commit()
        flash('Gênero musical adicionado com sucesso!', 'success')
        return redirect(url_for('listar_generos'))

@app.route('/genero/deletar/<int:id>', methods=['POST'])
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

@app.route('/pesquisar', methods=['GET'])
def pesquisar():
    search_query = request.args.get('search', '')

    resultados = {
        'vendas': [],
        'vinis': [],
        'clientes': []
    }

    if search_query:
        resultados['vendas'] = Venda.query.filter(
            (Venda.cliente.has(Cliente.Nome.like(f"%{search_query}%"))) |
            (Venda.itens_venda.any(ItensVenda.vinil.has(Vinil.Titulo.like(f"%{search_query}%")))) |
            (Venda.DataVenda.like(f"%{search_query}%"))
        ).all()

        resultados['vinis'] = Vinil.query.filter(
            (Vinil.Titulo.like(f"%{search_query}%")) |
            (Vinil.Artista.like(f"%{search_query}%"))
        ).all()

        resultados['clientes'] = Cliente.query.filter(
            (Cliente.Nome.like(f"%{search_query}%")) |
            (Cliente.Email.like(f"%{search_query}%")) |
            (Cliente.Telefone.like(f"%{search_query}%"))
        ).all()

    return render_template('pesquisar.html', resultados=resultados, search=search_query)

if __name__ == '__main__':
    app.run(debug=True)