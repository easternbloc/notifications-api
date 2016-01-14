from flask import (jsonify, request)
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound
from app.dao.services_dao import get_model_services
from app.dao.users_dao import (
    get_model_users, save_model_user, delete_model_user)
from app.schemas import (
    user_schema, users_schema, service_schema, services_schema)
from .. import user
from app import db


# TODO auth to be added
@user.route('/', methods=['POST'])
def create_user():
    user, errors = user_schema.load(request.get_json())
    if errors:
        return jsonify(result="error", message=errors), 400
    save_model_user(user)
    return jsonify(data=user_schema.dump(user).data), 201


# TODO auth to be added
@user.route('/<int:user_id>', methods=['PUT', 'DELETE'])
def update_user(user_id):
    try:
        user = get_model_users(user_id=user_id)
    except DataError:
        return jsonify(result="error", message="Invalid user id"), 400
    except NoResultFound:
        return jsonify(result="error", message="User not found"), 404
    if request.method == 'DELETE':
        status_code = 200
        delete_model_user(user)
    else:
        status_code = 200
        # TODO there has got to be a better way to do the next three lines
        update_user, errors = user_schema.load(request.get_json())
        if errors:
            return jsonify(result="error", message=errors), 400
        update_dict, errors = user_schema.dump(update_user)
        # TODO FIX ME
        # Remove update_service model which is added to db.session
        db.session.rollback()
        save_model_user(user, update_dict=update_dict)
    return jsonify(data=user_schema.dump(user).data), status_code


# TODO auth to be added.
@user.route('/<int:user_id>', methods=['GET'])
@user.route('/', methods=['GET'])
def get_user(user_id=None):
    try:
        users = get_model_users(user_id=user_id)
    except DataError:
        return jsonify(result="error", message="Invalid user id"), 400
    except NoResultFound:
        return jsonify(result="error", message="User not found"), 404
    result = users_schema.dump(users) if isinstance(users, list) else user_schema.dump(users)
    return jsonify(data=result.data)


# TODO auth to be added
@user.route('/<int:user_id>/service', methods=['GET'])
@user.route('/<int:user_id>/service/<int:service_id>', methods=['GET'])
def get_service_by_user_id(user_id, service_id=None):
    try:
        user = get_model_users(user_id=user_id)
    except DataError:
        return jsonify(result="error", message="Invalid user id"), 400
    except NoResultFound:
        return jsonify(result="error", message="User not found"), 404

    try:
        services = get_model_services(user_id=user.id, service_id=service_id)
    except DataError:
        return jsonify(result="error", message="Invalid service id"), 400
    except NoResultFound:
        return jsonify(result="error", message="Service not found"), 404
    services, errors = services_schema.dump(services) if isinstance(services, list) else service_schema.dump(services)
    return jsonify(data=services)
