from flask import request, json
import datetime
import hashlib
from app.main.dao import user_dao
import jwt


def create_signature(headers, claims, api_key):
    return jwt.encode(claims, api_key, algorithm='HS256', headers=headers)


def decode_data(api_key, sign):
    return jwt.decode(sign, api_key, algorithms=['HS256'])


def get_token_from_headers(headers):
    #
    # Valid request HEADER
    # {'Authorization': 'NOTIFY [USER_ID:[VALID.JWT.TOKEN]]}
    #
    try:
        auth_header = headers.get('Authorization', '')
        token = auth_header.split(":")

        api_user_id = token[0]
        jwt_token = token[1]
        user = user_dao.retrieve_user(api_user_id)

        claims = decode_token(user.api_key, jwt_token)
    except Exception as e:
        print(e)
        return False

    if not valid_claims(claims, user):
        return False

    if auth_header[:7] != 'NOTIFY ':
        return False

    return auth_header[7:]


def decode_token(api_key, sign):
    return jwt.decode(sign, api_key, algorithms=['HS256'])


def valid_claims(claims, user):
    print(">>>Checking claims")
    claim_data = json.loads(json.dumps(claims))

    if claim_data['sub'] != user.user_name:
        print(">>>Incorrect subject")
        return False

    if claim_data['iss'] != user.org:
        print(">>>Incorrect issuer")
        return False

    if datetime.datetime.fromtimestamp(int(claim_data['iat'])) + datetime.timedelta(
            days=1) < datetime.datetime.utcnow():
        print(datetime.datetime.fromtimestamp(int(claim_data['iat'])))
        print(">>>Token expired")
        return False

    request_url = request.url_rule
    if claim_data['qsh'] != hashlib.sha256(str(request_url).encode()).hexdigest():
        print(">>>Request doesn't match")
        return False

    print(">>>OK")
    return True
