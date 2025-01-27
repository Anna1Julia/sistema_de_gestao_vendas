from flask import Flask, render_template, request, redirect, url_for, flash
from models import db
from models.genero import GeneroMusical
from models.vinil import Vinil
from models.cliente import Cliente
from models.venda import Venda, ItensVenda

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

@app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/vendas')
def listar_vendas():
    vendas = Venda.query.all()
    return render_template('vendas.html', vendas=vendas)

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
        db.session.commit()

        return redirect(url_for('listar_vinis'))

    return render_template('adicionar_vinil.html', generos=generos)

@app.route('/deletar_vinil/<int:id>', methods=['POST'])
def deletar_vinil(id):
    vinil = Vinil.query.get_or_404(id)
    db.session.delete(vinil)
    db.session.commit()
    return redirect(url_for('listar_vinis'))

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

@app.route('/cliente/deletar/<int:id>', methods=['POST'])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente deletado com sucesso!', 'success')
    else:
        flash('Cliente não encontrado!', 'error')
    return redirect(url_for('listar_clientes'))

@app.route('/venda/adicionar', methods=['GET', 'POST'])
def adicionar_venda():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        vinis_selecionados = request.form.getlist('vinis[]')
        quantidades = request.form.getlist('quantidades[]')
        
        nova_venda = Venda(IDCliente=cliente_id)
        db.session.add(nova_venda)
        db.session.commit()

        valor_total = 0
        for vinil_id, quantidade in zip(vinis_selecionados, quantidades):
            vinil = Vinil.query.get(vinil_id)
            if vinil:
                quantidade = int(quantidade)
                
                if quantidade > vinil.Estoque:
                    flash(f"Quantidade solicitada para '{vinil.Titulo}' excede o estoque disponível!", 'error')
                    return redirect(url_for('adicionar_venda'))
                
                preco_unitario = vinil.Preco
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
        return redirect(url_for('listar_vendas'))

    vinis = Vinil.query.all()
    clientes = Cliente.query.all()
    return render_template('adicionar_venda.html', clientes=clientes, vinis=vinis)

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
        db.session.delete(genero)
        db.session.commit()
        flash('Gênero excluído com sucesso!', 'success')
    return redirect(url_for('listar_generos'))

if __name__ == '__main__':
    app.run(debug=True)
