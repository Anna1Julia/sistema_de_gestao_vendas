from flask import Flask, redirect, url_for
from models import db
from routes import vinis_bp, clientes_bp, vendas_bp, generos_bp, pesquisa_bp, main_bp, usuario_bp
from flask_login import LoginManager
from models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('usuario.login'))

app.register_blueprint(vinis_bp, url_prefix='/vinis')
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(vendas_bp, url_prefix='/vendas')
app.register_blueprint(generos_bp, url_prefix='/generos')
app.register_blueprint(pesquisa_bp, url_prefix='/pesquisa')
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(usuario_bp, url_prefix='/usuario')

def criar_admin():
    with app.app_context():
        db.create_all()
        print("Banco de dados configurado!")

        if not Usuario.query.filter_by(Email="admin@email.com").first():
            admin = Usuario(
                Nome="Administrador",
                Email="admin@email.com",
                Senha=generate_password_hash("admin123", method='pbkdf2:sha256'),
                Tipo="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuário administrador criado!")

criar_admin()

if __name__ == '__main__':
    app.run(debug=True)
