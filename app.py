from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegistration


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:essaeasenha@localhost/bdtestes'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

api = Api(app)


# antes da primeira request execute
def criar_banco():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<string:user_id>')
api.add_resource(UserRegistration, '/cadastro')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)

    with app.app_context():
        criar_banco()

    app.run(debug=True)
