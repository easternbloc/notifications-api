from datetime import datetime, timedelta

from client.authentication import create_jwt_token
from flask import json, url_for, current_app
from app.dao.api_key_dao import get_unsigned_secrets, save_model_api_key, get_unsigned_secret
from app.models import ApiKey, Service


def test_should_not_allow_request_with_no_token(notify_api):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            response = client.get(url_for('service.get_service'))
            assert response.status_code == 401
            data = json.loads(response.get_data())
            assert data['error'] == 'Unauthorized, authentication token must be provided'


def test_should_not_allow_request_with_incorrect_header(notify_api):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': 'Basic 1234'})
            assert response.status_code == 401
            data = json.loads(response.get_data())
            assert data['error'] == 'Unauthorized, authentication bearer scheme must be used'


def test_should_not_allow_request_with_incorrect_token(notify_api, notify_db, notify_db_session, sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': 'Bearer 1234'})
            assert response.status_code == 403
            data = json.loads(response.get_data())
            assert data['error'] == 'Invalid token: signature'


def test_should_not_allow_incorrect_path(notify_api, notify_db, notify_db_session, sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            token = create_jwt_token(request_method="GET",
                                     request_path="/bad",
                                     secret=get_unsigned_secrets(sample_api_key.service_id)[0],
                                     client_id=sample_api_key.service_id)
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': "Bearer {}".format(token)})
            assert response.status_code == 403
            data = json.loads(response.get_data())
            assert data['error'] == 'Invalid token: request'


def test_should_not_allow_incorrect_method(notify_api, notify_db, notify_db_session, sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            token = __create_post_token(sample_api_key.service_id, {})
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': "Bearer {}".format(token)})
            assert response.status_code == 403
            data = json.loads(response.get_data())
            assert data['error'] == 'Invalid token: request'


def test_should_not_allow_invalid_secret(notify_api, notify_db, notify_db_session, sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            token = create_jwt_token(request_method="POST", request_path="/", secret="not-so-secret",
                                     client_id=sample_api_key.service_id)
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': "Bearer {}".format(token)})
            assert response.status_code == 403
            data = json.loads(response.get_data())
            assert data['error'] == 'Invalid token: signature'


def test_should_allow_valid_token(notify_api, notify_db, notify_db_session, sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            token = __create_get_token(sample_api_key.service_id)
            response = client.get(url_for('service.get_service', service_id=sample_api_key.service_id),
                                  headers={'Authorization': 'Bearer {}'.format(token)})
            assert response.status_code == 200


def test_should_allow_valid_token_for_request_with_path_params(notify_api, notify_db, notify_db_session,
                                                               sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            token = __create_get_token(sample_api_key.service_id)
            response = client.get(url_for('service.get_service', service_id=sample_api_key.service_id),
                                  headers={'Authorization': 'Bearer {}'.format(token)})
            assert response.status_code == 200


def test_should_allow_valid_token_when_service_has_multiple_keys(notify_api, notify_db, notify_db_session,
                                                                 sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = {'service_id': sample_api_key.service_id, 'name': 'some key name'}
            api_key = ApiKey(**data)
            save_model_api_key(api_key)
            token = __create_get_token(sample_api_key.service_id)
            response = client.get(url_for('service.get_service', service_id=sample_api_key.service_id),
                                  headers={'Authorization': 'Bearer {}'.format(token)})
            assert response.status_code == 200


JSON_BODY = json.dumps({
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
})


def test_should_allow_valid_token_with_post_body(notify_api, notify_db, notify_db_session, sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            service = Service.query.get(sample_api_key.service_id)
            data = {'name': 'new name',
                    'users': [service.users[0].id],
                    'limit': 1000,
                    'restricted': False,
                    'active': False}

            token = create_jwt_token(
                request_method="PUT",
                request_path=url_for('service.update_service', service_id=sample_api_key.service_id),
                secret=get_unsigned_secret(sample_api_key.id),
                client_id=sample_api_key.service_id,
                request_body=json.dumps(data)
            )
            headers = [('Content-Type', 'application/json'), ('Authorization', 'Bearer {}'.format(token))]
            response = client.put(
                url_for('service.update_service', service_id=service.id),
                data=json.dumps(data),
                headers=headers)
            assert response.status_code == 200


def test_should_not_allow_valid_token_with_invalid_post_body(notify_api, notify_db, notify_db_session, sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            token = __create_post_token(sample_api_key.service_id, JSON_BODY)
            response = client.post(url_for('service.create_service'),
                                   data="spurious",
                                   headers={'Authorization': 'Bearer {}'.format(token)})
            assert response.status_code == 403
            data = json.loads(response.get_data())
            assert data['error'] == 'Invalid token: payload'


def test_authentication_passes_admin_client_token(notify_api,
                                                  notify_db,
                                                  notify_db_session,
                                                  sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            token = create_jwt_token(request_method="GET",
                                     request_path=url_for('service.get_service'),
                                     secret=current_app.config.get('ADMIN_CLIENT_SECRET'),
                                     client_id=current_app.config.get('ADMIN_CLIENT_USER_NAME'))
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': 'Bearer {}'.format(token)})
            assert response.status_code == 200


def test_authentication_passes_when_service_has_multiple_keys_some_expired(notify_api,
                                                                           notify_db,
                                                                           notify_db_session,
                                                                           sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            exprired_key = {'service_id': sample_api_key.service_id, 'name': 'expired_key',
                            'expiry_date': datetime.now()}
            expired_api_key = ApiKey(**exprired_key)
            save_model_api_key(expired_api_key)
            another_key = {'service_id': sample_api_key.service_id, 'name': 'another_key'}
            api_key = ApiKey(**another_key)
            save_model_api_key(api_key)
            token = create_jwt_token(request_method="GET",
                                     request_path=url_for('service.get_service'),
                                     secret=get_unsigned_secret(api_key.id),
                                     client_id=sample_api_key.service_id)
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': 'Bearer {}'.format(token)})
            assert response.status_code == 200


def test_authentication_returns_token_expired_when_service_uses_expired_key_and_has_multiple_keys(notify_api,
                                                                                                  notify_db,
                                                                                                  notify_db_session,
                                                                                                  sample_api_key):
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            expired_key = {'service_id': sample_api_key.service_id, 'name': 'expired_key'}
            expired_api_key = ApiKey(**expired_key)
            save_model_api_key(expired_api_key)
            another_key = {'service_id': sample_api_key.service_id, 'name': 'another_key'}
            api_key = ApiKey(**another_key)
            save_model_api_key(api_key)
            token = create_jwt_token(request_method="GET",
                                     request_path=url_for('service.get_service'),
                                     secret=get_unsigned_secret(expired_api_key.id),
                                     client_id=sample_api_key.service_id)
            # expire the key
            expire_the_key = {'id': expired_api_key.id,
                              'service_id': sample_api_key.service_id,
                              'name': 'expired_key',
                              'expiry_date': datetime.now() + timedelta(hours=-2)}
            save_model_api_key(expired_api_key, expire_the_key)
            response = client.get(url_for('service.get_service'),
                                  headers={'Authorization': 'Bearer {}'.format(token)})
            assert response.status_code == 403
            data = json.loads(response.get_data())
            assert data['error'] == 'Invalid token: signature'


def __create_get_token(service_id):
    if service_id:
        return create_jwt_token(request_method="GET",
                                request_path=url_for('service.get_service', service_id=service_id),
                                secret=get_unsigned_secrets(service_id)[0],
                                client_id=service_id)
    else:
        return create_jwt_token(request_method="GET",
                                request_path=url_for('service.get_service'),
                                secret=get_unsigned_secrets(service_id)[0],
                                client_id=service_id)


def __create_post_token(service_id, request_body):
    return create_jwt_token(
        request_method="POST",
        request_path=url_for('service.create_service'),
        secret=get_unsigned_secrets(service_id)[0],
        client_id=service_id,
        request_body=request_body
    )
