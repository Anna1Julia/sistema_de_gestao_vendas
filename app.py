from flask import Flask
from models import db
from routes import vinis, clientes, vendas, generos, pesquisa, main, usuario

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

app.register_blueprint(vinis, url_prefix='/vinis')
app.register_blueprint(clientes, url_prefix='/clientes')
app.register_blueprint(vendas, url_prefix='/vendas')
app.register_blueprint(generos, url_prefix='/generos')
app.register_blueprint(pesquisa, url_prefix='/pesquisa')
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(usuario, url_prefix='/usuario')

if __name__ == '__main__':
    app.run(debug=True)
