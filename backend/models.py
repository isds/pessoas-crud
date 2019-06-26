from database import db


def dump_date(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")


class Telefone(db.Model):
    __tablename__ = 'telefones'

    id = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.String())
    numero = db.Column(db.String())
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'))

class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    cpf = db.Column(db.String())
    datanascimento = db.Column(db.Date())
    email = db.Column(db.String())
    telefones = db.relationship('Telefone', backref='telefones')
