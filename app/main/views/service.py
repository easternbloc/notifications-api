from flask import jsonify, request
from .. import main
from app.main.auth import token_auth

from app.main.dao import service_dao, user_dao


@main.route('/services', methods=['GET'])
def fetch_services():
    services = service_dao.retrieve_all_services()

    return jsonify(
        service=[service.serialize() for service in services]
    )


@main.route('/service', methods=['POST'])
def add_service():
    # if POST body encrypted and uses JWT format
    # we use PyJWT to decrypt
    if body_encrypted_as_jwt:
        post_body = _get_body()
    else:
        post_body = request.data

    service_dao.add_service(post_body)

    return ""


def body_encrypted_as_jwt():
    return True


def _get_body():
    jwt_token = token_auth.get_token_from_headers(request.headers)
    token = jwt_token.split(":")

    user_id = token[0]
    print(">>> API_USER_ID", token[0])

    user = user_dao.retrieve_user(user_id)

    api_key = user.api_key

    print(">>>Encrypted POST request body: ", request.data)

    post_body = token_auth.decode_data(api_key, request.data)
    print(">>>Decrypted POST Body: ", post_body)

    return post_body
