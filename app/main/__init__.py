from flask import Blueprint, current_app, request, abort
from app.main.dao import user_dao
from app.main.auth.token_auth import get_token_from_headers

main = Blueprint('main', __name__)


def requires_authentication():
    if current_app.config['AUTH_REQUIRED']:
        incoming_token = get_token_from_headers(request.headers)

        if not incoming_token:
            abort(401)


main.before_request(requires_authentication)

from app.main.views import service
