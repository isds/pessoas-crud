from flask_restful import Api, Resource

from resources import PessoaResource, TelefoneResource
from database import db


class Index(Resource):
    def get(self):
        return {'message': 'Pessoas CRUD API Responding.'}


api = Api()


def configure_api(app):
    # Add the test api route
    api.add_resource(Index, '/')

    # Pessoa Routes
    api.add_resource(PessoaResource, '/pessoas', '/pessoas/<pessoa_id>')
    api.add_resource(TelefoneResource, '/telefones',
                     '/telefones/<telefone_id>')

    api.init_app(app)
