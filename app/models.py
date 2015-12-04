from application import db


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    limit = db.Column(db.BigInteger, index=False, unique=False, nullable=False)
    restricted = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    def serialize(self):
        serialized = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at,
            'active': self.active,
            'limit': self.limit,
            'restricted': self.restricted
        }

        return serialized


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(255), nullable=False)
    org = db.Column(db.String(255), nullable=False)

    def serialize(self):
        serialized = {
            'id': self.id,
            'user_name': self.user_name,
            'api_key': self.api_key,
            'org': self.org
        }

        return serialized
