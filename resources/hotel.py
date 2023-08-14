from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    """
    Criação de um objeto `query_params` para
    lidar com os parâmetros de consulta
    """
    query_params = reqparse.RequestParser()

    """
    Definição dos argumentos que podem ser passados
    como parâmetros de consulta.
    path /hoteis?cidade==Rio de Janeiro&estrelas_min=4&diraria=300
    """
    query_params.add_argument("cidade",
                              type=str, default="", location="args")

    query_params.add_argument("estrelas_min",
                              type=float, default=0, location="args")

    query_params.add_argument("estrelas_max",
                              type=float, default=5, location="args")

    query_params.add_argument("diaria_min",
                              type=float, default=0, location="args")

    query_params.add_argument("diaria_max",
                              type=float, default=10000, location="args")

    query_params.add_argument("site_id",
                              type=int, default=0, location="args")

    query_params.add_argument("limit",
                              type=float, default=50, location="args")

    query_params.add_argument("offset",
                              type=float, default=0, location="args")

    def get(self):
        # Parse dos parâmetros de consulta com base nas definições anteriores
        filters = Hoteis.query_params.parse_args()

        # Criação de uma query inicial usando o modelo HotelModel
        query = HotelModel.query

        # Aplicação de filtros à query baseados nos parâmetros de consulta
        if filters["cidade"]:
            query = query.filter(
                HotelModel.cidade == filters["cidade"])
        if filters["estrelas_min"]:
            query = query.filter(
                HotelModel.estrelas >= filters["estrelas_min"])
        if filters["estrelas_max"]:
            query = query.filter(
                HotelModel.estrelas <= filters["estrelas_max"])
        if filters["diaria_min"]:
            query = query.filter(
                HotelModel.diaria >= filters["diaria_min"])
        if filters["diaria_max"]:
            query = query.filter(
                HotelModel.diaria <= filters["diaria_max"])
        if filters["limit"]:
            query = query.limit(filters["limit"])
        if filters["offset"]:
            query = query.offset(filters["offset"])
        if filters["site_id"]:
            query = query.filter(
                HotelModel.cidade == filters["site_id"])

        # Execução da query e geração da lista de resultados no formato JSON
        return {"hoteis": [hotel.json() for hotel in query]}


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
    argumentos.add_argument(
        'site_id', type=int, required=True,
        help="Every hotel needs to be linked with site"
    )

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

        if not SiteModel.find_by_id(dados['site_id']):
            return {
                'message': 'The hotel must be associated to a valid site id.'
            }, 400

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
