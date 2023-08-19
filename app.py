from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegistration, UserLogin, UserLogout, UserConfirm
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:essaeasenha@localhost/bdtestes'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

api = Api(app)

# gerenciar login
# Configura a chave secreta do JWT
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

jwt = JWTManager(app)


# antes da primeira request execute
def criar_banco():
    banco.create_all()


# verificar se o token ta ou não na blacklist
@jwt.token_in_blocklist_loader
def verica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message': 'You have been logged out.'}), 401


api.add_resource(User, '/usuarios/<string:user_id>')
api.add_resource(UserRegistration, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)

    with app.app_context():
        criar_banco()

    app.run(debug=True)
