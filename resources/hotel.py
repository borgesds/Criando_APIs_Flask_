"""
==> Base
from flask_restful import Resource, reqparse


hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 450.56,
        'cidade': 'São Paulo'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 3.8,
        'diaria': 290.36,
        'cidade': 'Belo Horizonte'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 4.9,
        'diaria': 550.88,
        'cidade': 'Rio Grande do Sul'
    },
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            return hotel

        return {'message': 'Hotel not found'}, 404  # Not found

    def post(self, hotel_id):
        # Pegas os argumentos la em cima
        dados = Hotel.argumentos.parse_args()

        novo_hotel = {
            'hotel_id': hotel_id,
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }

        hoteis.append(novo_hotel)

        return novo_hotel, 200

    def put(self, hotel_id):
        # Pegas os argumentos la em cima
        dados = Hotel.argumentos.parse_args()

        novo_hotel = {'hotel_id': hotel_id, **dados}

        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            hotel.update(novo_hotel)

            return novo_hotel, 200

        hoteis.append(novo_hotel)

        return novo_hotel, 201  # created

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]

        return {'message': 'Hotel deleted!!!'}
"""
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return hotel.json()

        return {'message': 'Hotel not found'}, 404  # Not found

    def post(self, hotel_id):
        # buscando a função la em models.hotel
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id {hotel_id} already exists'}, 400

        # Pegas os argumentos la em cima
        dados = Hotel.argumentos.parse_args()

        # chama a class de inciação (args, kwargs)
        hotel = HotelModel(hotel_id, **dados)

        # buscando a função la em models.hotel
        hotel.save_hotel()

        return hotel.json(), 201

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
        hotel.save_hotel()

        return hotel.json(), 201  # created

    def delete(self, hotel_id):
        

        return {'message': 'Hotel deleted!!!'}
