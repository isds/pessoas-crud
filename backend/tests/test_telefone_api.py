from database import db
from application import app
from models import Pessoa, Telefone
from resources import get_pessoa_by_id
import json
from pytest import mark


class TestTelefoneAPI:
    def setup_method(self):
        self.db = db

        app.config['TESTING'] = True

        self.cpf = '0000001111-11'

        self.pessoa = Pessoa(
            nome='Joe Doe For Tests',
            email='joedoe@test.com',
            cpf=self.cpf,
            datanascimento='1993-01-23'
        )

        self.telefone = Telefone(
            ddd='85',
            numero='32861556',
            pessoa_id=self.pessoa.id
        )

        self.test_app = app
        self.client = self.test_app.test_client()

    def teardown_method(self):
        with self.test_app.app_context():
            pessoa = Pessoa.query.filter_by(cpf=self.cpf).first()
            if pessoa:
                self.db.session.delete(pessoa)
                self.db.session.commit()
            telefone = Telefone.query.filter_by(numero='32861556').first()
            if telefone:
                self.db.session.delete(telefone)
                self.db.session.commit()

    def test_function_get_telefone_by_id(self):
        with self.test_app.app_context():
            self.db.session.add(self.telefone)
            self.db.session.commit()

            telefone = Telefone.query.filter_by(
                numero=self.telefone.numero).first()
            assert telefone.ddd == self.telefone.ddd
            assert telefone.numero == self.telefone.numero
            assert telefone.pessoa_id == self.telefone.pessoa_id

    def test_get_telefone_by_id(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.add(self.telefone)
            self.db.session.commit()

            response = self.client.get(f'/telefones/{self.telefone.id}')
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 200, error
            assert type(_response['data']) == dict, error
            assert _response['message'] == 'Recursos retornados com sucesso.', error

    def test_get_telefone_by_pessoa(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.add(self.telefone)
            self.db.session.commit()

            response = self.client.get(
                f'/pessoas', query_string={'pessoa_id': self.pessoa.id}
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 200, error
            assert type(_response['data']) == list, error
            assert len(_response['data']) > 0, error
            assert _response['message'] == 'Recursos retornados com sucesso.', error

    def test_get_telefones(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.add(self.telefone)
            self.db.session.add(self.telefone)
            self.db.session.commit()

            response = self.client.get(
                f'/pessoas'
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 200, error
            assert type(_response['data']) == list, error
            # since cpf is unique only one row must be returned
            assert len(_response['data']) > 0, error
            assert _response['message'] == 'Recursos retornados com sucesso.', error

    def test_add_contact(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()

            data = {
                'ddd': '81',
                'numero': '77777788',
                'pessoa_id': self.pessoa.id
            }

            response = self.client.post(
                '/telefones', json=data
            )
            _response = json.loads(response.data)
            error = _response.get('description')
            assert response.status_code == 201, error

            telefone = Telefone.query.filter_by(numero='77777788').first()

            assert telefone != None, error
            assert telefone.numero == '77777788'

            self.db.session.delete(telefone)
            self.db.session.commit()

    def test_update_contact(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.add(self.telefone)
            self.db.session.commit()

            # pessoa = Pessoa.query.filter_by(cpf='0000001111-11').first()
            new_data = {'numero': '090910909'}
            response = self.client.put(
                f'/telefones/{self.telefone.id}', json=new_data
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 210, error
            assert _response['message'] == 'Registro atualizado com sucesso.', error
            assert type(_response['data']) == dict, error
            assert _response['data']['numero'] == new_data['numero'], error

            self.db.session.delete(self.pessoa)
            self.db.session.delete(self.telefone)
            self.db.session.commit()

    def test_delete_contact(self):
        with self.test_app.app_context():
            self.db.session.add(self.pessoa)
            self.db.session.commit()
            pessoa = Telefone.query.filter_by(numero='32861556').first()

            response = self.client.delete(
                f'/telefones/{pessoa.id}'
            )
            _response = json.loads(response.data)
            error = _response.get('description')

            assert response.status_code == 202, error
