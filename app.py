from flask import Flask
from models import db
from flask_login import LoginManager

from routes.vinis_bp import vinis_bp
from routes.clientes_bp import clientes_bp
from routes.vendas_bp import vendas_bp
from routes.generos_bp import generos_bp
from routes.main_bp import main_bp
from routes.usuario_bp import usuario_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sua_conexao_com_o_banco'
app.config['SECRET_KEY'] = 'sua_chave_secreta'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'usuario.login'

app.register_blueprint(vinis_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(vendas_bp)
app.register_blueprint(generos_bp)
app.register_blueprint(main_bp)
app.register_blueprint(usuario_bp)

from routes.pesquisa_bp import pesquisa_bp
app.register_blueprint(pesquisa_bp)

if __name__ == "__main__":
    app.run(debug=True)
