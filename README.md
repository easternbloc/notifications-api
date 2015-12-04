https://travis-ci.org/alphagov/notifications-api.svg

# notifications-api
Notifications api
Application for the notification api.

Read and write notifications/status queue.
Get and update notification status.

# Using JWT

To run test client:

```
python jwt_test_client.py 
```

## JSON Web Token

- <http://jwt.io/introduction/>
- <http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html>


## PyJWT

[JSON Web Token implementation](https://github.com/jpadilla/pyjwt)


## JWT Token structure

```headers = {
    "type": "JWT",
    "alg": "HS256"
}

claims = {
    'iss': 'gov.uk',
    'iat': datetime.utcnow(),
    'sub': user email,
    'qsh': request_url_hash
}
```