from application import application
from app.main.auth import token_auth
import hashlib
from datetime import datetime

import unittest

API_KEY = "1234asdf5678"

API_USER_ID = '1'


class TestCase(unittest.TestCase):
    def test_service_get_api_no_token(self):
        print(">>>Testing request without JWT")
        tester = application.test_client(self)
        resp = tester.get('/services', content_type='application/json')

        print(">>>RESPONSE:", resp)
        self.assertEqual(resp.status_code, 401)

    def test_service_get_api(self):
        print(">>>Testing GET request with JWT")
        tester = application.test_client(self)

        request_url = "/services"
        request_url_hash = hashlib.sha256(request_url.encode()).hexdigest()

        headers = {
            "type": "JWT",
            "alg": "HS256"
        }

        claims = {
            'iss': 'gov.uk',
            'iat': datetime.utcnow(),
            'sub': 'test@user.com',
            'qsh': request_url_hash
        }

        sign = token_auth.create_signature(headers=headers, claims=claims, api_key=API_KEY)

        headers = {'Authorization': 'NOTIFY ' + API_USER_ID + ":" + sign.decode()}
        print(">> Request header: ", headers)
        resp = tester.get(request_url, content_type='application/json', headers=headers)

        print(resp.get_data())

        self.assertEqual(resp.status_code, 200)

    def test_service_post_api(self):
        tester = application.test_client(self)

        request_url = "/service"
        request_url_hash = hashlib.sha256(request_url.encode()).hexdigest()

        # JWT for request header
        headers = {
            "type": "JWT",
            "alg": "HS256"
        }

        claims = {
            'iss': 'gov.uk',
            'iat': datetime.utcnow(),
            'sub': 'test@user.com',
            'qsh': request_url_hash
        }

        sign = token_auth.create_signature(headers=headers, claims=claims, api_key=API_KEY)

        headers = {'Authorization': 'NOTIFY ' + API_USER_ID + ":" + sign.decode()}
        print(">> Request header: ", headers)

        # If POST body will be encrypted using JWT standard it will require two parts:
        # - JWT head
        # and
        # - custom body

        head = {
            "type": "JWT",
            "alg": "HS256"
        }

        service = {
            'service':
                {
                    'user_id': str(API_USER_ID),
                    'name': 'TEST SERVICE',
                    'created_at': str(datetime.utcnow()),
                    'active': str(True),
                    'limit': str(100),
                    'restricted': str(True)
                }
        }

        msg = token_auth.create_signature(headers=head, claims=service, api_key=API_KEY)

        msg = msg.decode()
        print(">>>POST body: ", msg)

        # hash_alg = hashlib.sha256
        # key = API_KEY.encode('utf-8')
        # digest = hmac.new(key, payload, hash_alg).digest()
        # signature = base64url_encode(digest)
        # print(">>> Signature: ", signature)

        resp = tester.post('/service', content_type='application/json', headers=headers, data=msg)

        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
