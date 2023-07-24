from flask_restful import Resource
from models.usuario import UserModel


class User(Resource):

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
