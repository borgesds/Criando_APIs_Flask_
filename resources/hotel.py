from flask_restful import Resource


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
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

        return {'message': 'Hotel not found'}, 404  # Not found

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
