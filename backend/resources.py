from flask_restful import Resource
from database import db
from models import Pessoa, Telefone
from schemas import PessoaSchema, TelefoneSchema
from flask import request
from flask_cors import cross_origin
from responses import (response_exception, response_ok, response_resource_created,
                       response_resource_updated, response_resource_deleted,
                       response_data_invalid)


def get_pessoa_by_id(pessoa_id):
    try:
        return Pessoa.query.filter_by(id=pessoa_id).first()
    except Exception as ex:
        return response_exception('Pessoa', description=ex.__str__())


def get_telefone_by_id(telefone_id):
    try:
        return Telefone.query.filter_by(id=telefone_id).first()
    except Exception as ex:
        return response_exception('Telefone', description=ex.__str__())


class PessoaResource(Resource):
    def post(self, *args, **kwargs):
        request_data = request.get_json() or None
        pessoa_schema = PessoaSchema()

        # If no data is passed return message
        if request_data is None:
            return response_data_invalid('Pessoa', 'Nenhum dado foi informado')

        data, errors = pessoa_schema.load(request_data)

        # Return errors if they exists
        if errors:
            return response_data_invalid('Pessoa', errors)

        try:
            pessoa = data
            db.session.add(pessoa)
            db.session.commit()
        except Exception as ex:
            return response_exception('Pessoa', description=ex.__str__())

        # Makes a dump from saved model
        result = pessoa_schema.dump(pessoa)

        return response_resource_created('Pessoa', 'Registro criado com sucesso.', data=result.data)

    def get(self, pessoa_id=None):
        pessoa_schema = PessoaSchema()
        if pessoa_id:
            pessoa = get_pessoa_by_id(pessoa_id)

            if not isinstance(pessoa, Pessoa):
                return pessoa  # if its a error returns

            # translates data
            data, error = pessoa_schema.dump(pessoa)

            if error:  # If any error is returned sends back as a http response
                return response_exception(
                    # TODO check error responses
                    'Pessoa', 'Dados inválidos', description=erro.__str__()
                )
            extra = {'total': 1}

        else:
            try:
                query = Pessoa.query
                if request.args:
                    _nome = request.args.get('nome')
                    if _nome:
                        query = query.filter(Pessoa.nome.like(f'%{_nome}%'))
                    _cpf = request.args.get('cpf')
                    if _cpf:
                        query = query.filter(Pessoa.cpf.like(f'%{_cpf}%'))

            except Exception as ex:
                return response_exception('Pessoa', description=ex.__str__())

            data, errors = [], []
            for pessoa in query.all():  # for each meal
                _data, _error = pessoa_schema.dump(pessoa)
                data.append(_data)
                if _error:  # Add error only if exists
                    errors.append(_error)

            if errors:  # If any error is returned sends back as a http response
                return response_exception('Pessoa', description=erros[0].__str__())

            extra = {'total': len(data)}
        return response_ok(
            'Pessoa', 'Recursos retornados com sucesso.',  data=data, **extra
        )

    def put(self, pessoa_id):
        pessoa_schema = PessoaSchema()
        request_data = request.get_json() or None

        pessoa = get_pessoa_by_id(pessoa_id)
        if not isinstance(pessoa, Pessoa):
            return pessoa

        data, error = pessoa_schema.load(request_data, instance=pessoa)
        if error:
            return response_data_invalid('Pessoa', error.__str__())

        try:
            pessoa.nome = data.nome if data.nome else pessoa.nome
            pessoa.cpf = data.cpf if data.cpf else pessoa.cpf
            pessoa.email = data.email if data.email else pessoa.email
            pessoa.datanascimento = data.datanascimento if data.datanascimento else pessoa.datanascimento

            db.session.commit()
        except Exception as e:
            return response_exception('Pessoa', description=e.__str__())

        result = pessoa_schema.dump(pessoa)
        return response_resource_updated('Pessoa', 'Registro atualizado com sucesso.',  data=result.data)

    def delete(self, pessoa_id):
        pessoa = get_pessoa_by_id(pessoa_id)
        if not isinstance(pessoa, Pessoa):
            return pessoa

        try:
            db.session.delete(pessoa)
            db.session.commit()
        except Exception as ex:
            return response_exception('Pessoa', msg='Id inválido', description=ex.__str__())

        return response_resource_deleted('Pessoa', 'Registro removido com sucesso.')


class TelefoneResource(Resource):
    def post(self, *args, **kwargs):
        request_data = request.get_json() or None
        telefone_schema = TelefoneSchema()

        # If no data is passed return message
        if request_data is None:
            return response_data_invalid('Telefone', msg='Nenhum dado foi informado.')

        data, errors = telefone_schema.load(request_data)

        # Return errors if they exists
        if errors:
            return response_data_invalid('Telefone', errors)

        try:
            telefone = data

            db.session.add(telefone)
            db.session.commit()
        except Exception as ex:
            return response_exception('Telefone', description=ex.__str__())

        # Makes a dump from saved model to return in response and show persisted data.
        result = telefone_schema.dump(telefone)

        return response_resource_created('Telefone', 'Registro criado com sucesso.', data=result.data)

    def get(self, telefone_id=None):
        telefone_schema = TelefoneSchema()
        if telefone_id:
            telefone = get_telefone_by_id(telefone_id)

            if not isinstance(telefone, Telefone):
                return telefone  # if its a error returns

            # translates data
            data, error = telefone_schema.dump(telefone)

            if error:  # If any error is returned sends back as a http response
                return response_exception(
                    # TODO check error responses
                    'Telefone', 'Dados inválidos', description=erro.__str__()
                )
            extra = {'total': 1}

        else:

            try:
                query = Telefone.query
                if request.args:
                    _pessoa_id = request.args.get('pessoa_id')
                    if _pessoa_id:
                        query = query.filter_by(pessoa_id=_pessoa_id)

            except Exception as ex:
                return response_exception('Pessoa', description=ex.__str__())
                # return response_exception('Pessoa', description='Erro ao fazer busca.')

            data, errors = [], []
            for telefone in query.all():  # for each meal
                _data, _error = telefone_schema.dump(telefone)
                data.append(_data)
                if _error:  # Add error only if exists
                    errors.append(_error)

            if errors:  # If any error is returned sends back as a http response
                return response_exception('Telefone', description=erros[0].__str__())

            extra = {'total': len(data)}
        return response_ok(
            'Telefone', 'Recursos retornados com sucesso.',  data=data, **extra
        )

    def put(self, telefone_id=None):
        telefone_schema = TelefoneSchema()
        request_data = request.get_json() or None

        telefone = get_telefone_by_id(telefone_id)
        if not isinstance(telefone, Telefone):
            return telefone

        data, error = telefone_schema.load(request_data)
        if error:
            return response_data_invalid('Telefone', error.__str__())

        try:
            telefone.ddd = data.ddd if data.ddd else telefone.ddd
            telefone.numero = data.numero if data.numero else telefone.numero
            telefone.pessoa_id = data.pessoa_id if data.pessoa_id else telefone.pessoa_id

            db.session.commit()
        except Exception as e:
            return response_exception('Telefone', description=e.__str__())

        result = telefone_schema.dump(telefone)
        return response_resource_updated('Telefone', 'Registro atualizado com sucesso.',  data=result.data)

    def delete(self, telefone_id=None):
        telefone = get_telefone_by_id(telefone_id)
        if not isinstance(telefone, Telefone):
            return telefone

        try:
            db.session.delete(telefone)
            db.session.commit()
        except Exception as ex:
            return response_exception('Telefone', msg='Id inválido', description=ex.__str__())

        return response_resource_deleted('Telefone', 'Registro removido com sucesso.')
