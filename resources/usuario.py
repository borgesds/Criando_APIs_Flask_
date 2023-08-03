from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import hmac
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument(
    'login',
    type=str,
    required=True,
    help="The field 'login' not blank"
)
atributos.add_argument(
    'senha',
    type=str,
    required=True,
    help="The field 'senha' not blank"
)


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            return user.json()

        return {'message': 'User not found'}, 404  # Not found

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            try:
                user.delete_user()
            except Exception:
                return {
                    'message': 'An error occurred trying to delete user'
                }, 500  # Internal Server Error

            return {'message': 'User deleted successfully'}

        return {'message': 'User not found'}


class UserRegistration(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {
                'message': f'The login *{dados["login"]}* already exists.'
            }

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User crated successfully!'}, 201  # Created


class UserLogin(Resource):
    # /login
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)

            return {'access': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200
