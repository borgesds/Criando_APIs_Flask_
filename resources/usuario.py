from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_hotel(user_id)

        if user:
            return user.json()

        return {'message': 'Hotel not found'}, 404  # Not found

    def delete(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            try:
                user.delete_user()
            except Exception:
                return {
                    'message': 'An error occurred trying to delete hotel'
                }, 500  # Internal Server Error

            return {'message': 'Hotel deleted successfully'}

        return {'message': 'Hotel not found'}


class UserRegistration(Resource):
    # /cadastro
    def post(self):
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
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {
                'message': f'The login *{dados["login"]}* already exists.'
            }

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'Yser crated successfully!'}, 201  # Created
