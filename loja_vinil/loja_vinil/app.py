
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Genero, Vinil, Cliente, Venda
from models import db
from models.genero import Genero
from models.vinil import Vinil
from models.cliente import Cliente
from models.venda import Venda

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)


app = Flask(__name__)
app.config.from_object('config.Config')  
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vinis', methods=['GET'])
def listar_vinis():
    genero = request.args.get('genero')
    preco_min = request.args.get('preco_min', type=float)
    preco_max = request.args.get('preco_max', type=float)
    query = Vinil.query
    if genero:
        query = query.filter(Vinil.genero_id == genero)
    if preco_min is not None:
        query = query.filter(Vinil.preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Vinil.preco <= preco_max)
    vinis = query.all()
    generos = Genero.query.all()
    return render_template('vinis.html', vinis=vinis, generos=generos)

@app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/vendas')
def listar_vendas():
    vendas = Venda.query.all()
    return render_template('vendas.html', vendas=vendas)

if __name__ == '__main__':
    app.run(debug=True)
