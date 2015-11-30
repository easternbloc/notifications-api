from application import db


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    token_id = db.Column(db.BigInteger, db.ForeignKey('token.id'), index=True, unique=True)
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    limit = db.Column(db.BigInteger, index=False, unique=False, nullable=False)
    restricted = db.Column(db.Boolean, index=False, unique=False, nullable=False)
