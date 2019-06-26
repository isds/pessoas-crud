from models import Pessoa, Telefone
from marshmallow_sqlalchemy import ModelSchema
from database import db


class PessoaSchema(ModelSchema):
    class Meta:
        model = Pessoa
        sqla_session = db.Session


class TelefoneSchema(ModelSchema):
    class Meta:
        model = Telefone
        fields = ('ddd', 'id', 'numero', 'pessoa_id')
        sqla_session = db.Session
