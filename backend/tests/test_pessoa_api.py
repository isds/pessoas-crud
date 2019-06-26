from database import db
from application import app
from models import Pessoa
from resources import get_pessoa_by_id
import json


class TestPessoaAPI:
    def setup_method(self):
        self.cpf = '0000001111-11'
        self.nome = 'Joe Doe For Tests'
        self.pessoa = Pessoa(
            nome=self.nome,
            email='joedoe@test.com',
            cpf=self.cpf,
            datanascimento='1993-01-23'
        )
        app.config['TESTING'] = True

        self.test_app = app
        self.client = self.test_app.test_client()
        self.db = db

    def teardown_method(self):
        with self.test_app.app_context():
            pessoa = Pessoa.query.filter_by(cpf=self.cpf).first()
            if pessoa:
                self.db.session.delete(pessoa)
                self.db.session.commit()

    def test_function_get_pessoa_by_id(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()

            pessoa = Pessoa.query.filter_by(cpf=self.cpf).first()
            assert pessoa.nome == self.pessoa.nome
            assert pessoa.email == self.pessoa.email
            assert pessoa.datanascimento == self.pessoa.datanascimento

    def test_get_pessoa_by_id(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()

            response = self.client.get(f'/pessoas/{self.pessoa.id}')
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 200
            assert type(_response['data']) == dict, error
            assert _response['message'] == 'Recursos retornados com sucesso.', error

    def test_get_pessoa_by_nome(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()

            response = self.client.get(
                f'/pessoas', query_string={'nome': self.nome}
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 200, error
            assert type(_response['data']) == list, error
            assert len(_response['data']) > 0, error
            assert _response['message'] == 'Recursos retornados com sucesso.', error

    def test_get_pessoa_by_cpf(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()

            response = self.client.get(
                f'/pessoas', query_string={'cpf': self.cpf}
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 200, error
            assert type(_response['data']) == list, error
            # since cpf is unique only one row must be returned
            assert len(_response['data']) == 1, error
            assert _response['message'] == 'Recursos retornados com sucesso.', error

            pessoa = _response['data'][0]
            assert self.pessoa.nome == pessoa.get('nome')
            assert self.pessoa.cpf == pessoa.get('cpf')

    def test_add_contact(self):
        with self.test_app.app_context():

            data = {
                'nome': 'Joe Doe For Creation Test',
                'email': 'joedoe@test.com',
                'cpf': '1123455890-11',
                'datanascimento': '1993-01-23'
            }

            response = self.client.post(
                '/pessoas', json=data
            )
            _response = json.loads(response.data)
            error = _response.get('description')
            assert response.status_code == 201, error

            pessoa = Pessoa.query.filter_by(cpf='1123455890-11').first()

            assert pessoa != None, error
            assert pessoa.cpf == '1123455890-11'

            self.db.session.delete(pessoa)
            self.db.session.commit()

    def test_update_contact(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()

            # pessoa = Pessoa.query.filter_by(cpf='0000001111-11').first()
            new_data = {'nome': 'Novo Nome do Joe Doe'}
            response = self.client.put(
                f'/pessoas/{self.pessoa.id}', json=new_data
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 210, error
            assert _response['message'] == 'Registro atualizado com sucesso.', error
            assert type(_response['data']) == dict, error
            assert _response['data']['nome'] == new_data['nome'], error

            pessoa = Pessoa.query.filter_by(cpf='0000001111-11').first()
            # since cpf is unique only one row must be returned
            assert pessoa.nome == new_data['nome']

            self.db.session.delete(pessoa)
            self.db.session.commit()

    def test_delete_contact(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()
            pessoa = Pessoa.query.filter_by(cpf='0000001111-11').first()

            response = self.client.delete(
                f'/pessoas/{pessoa.id}'
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 202, error
