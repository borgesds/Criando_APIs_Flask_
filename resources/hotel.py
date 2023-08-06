from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from banco_mysql import criar_conexao


def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset
        }


# path /hoteis?cidade==Rio de Janeiro&estrelas_min=4&diraria=300
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offiset', type=float)


class Hoteis(Resource):
    def get(self):
        conn = criar_conexao('localhost', 'root', 'essaeasenha', 'bdtestes')
        cursor = conn.cursor()

        dados = path_params.parse_args()

        # receber so os dados validos
        dados_validos = {
            chave: dados[chave] for chave in dados if dados[chave] is not None
        }

        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            consulta = "SELECT * FROM hoteis \
                WHERE (estrelas > ? and estrelas < ?) \
                and (diaria > ? and diaria < ?) \
                LIMIT ? OFFSET ?"

            valores = tuple([parametros[chave] for chave in parametros])

            resultado = cursor.execute(consulta, valores)
        else:
            consulta = "SELECT * FROM hoteis \
                WHERE (estrelas > ? and estrelas < ?) \
                and (diaria > ? and diaria < ?) \
                and cidade = ? LIMIT ? OFFSET ?"

            valores = tuple([parametros[chave] for chave in parametros])

            resultado = cursor.execute(consulta, valores)

        return {
            'hoteis': [
                hotel.json() for hotel in HotelModel.query.all()
                ]
            }


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument(
        'nome', type=str, required=True,
        help="The field 'name' not blank"
    )
    argumentos.add_argument(
        'estrelas', type=float, required=True,
        help="The field 'estrelas' not blank"
    )
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return hotel.json()

        return {'message': 'Hotel not found'}, 404  # Not found

    @jwt_required()
    def post(self, hotel_id):
        # buscando a função la em models.hotel
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id {hotel_id} already exists'}, 400

        # Pegas os argumentos la em cima
        dados = Hotel.argumentos.parse_args()

        # chama a class de inciação (args, kwargs)
        hotel = HotelModel(hotel_id, **dados)

        try:
            # buscando a função la em models.hotel
            hotel.save_hotel()
        except Exception:
            return {
                'message': 'An internal error ocurred trying to save hotel'
            }, 500  # Internal Server Error

        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):
        # Pegas os argumentos la em cima
        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()

            return hotel_encontrado.json(), 200

        # caso não tenha, chama a class de inciação (args, kwargs)
        hotel = HotelModel(hotel_id, **dados)

        try:
            # buscando a função la em models.hotel
            hotel.save_hotel()
        except Exception:
            return {
                'message': 'An internal error ocurred trying to save hotel'
            }, 500  # Internal Server Error

        return hotel.json(), 201  # created

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except Exception:
                return {
                    'message': 'An error occurred trying to delete hotel'
                }, 500  # Internal Server Error

            return {'message': 'Hotel deleted successfully'}

        return {'message': 'Hotel not found'}
