https://travis-ci.org/alphagov/notifications-api.svg

# notifications-api
Notifications api
Application for the notification api.

Read and write notifications/status queue.
Get and update notification status.

# Using JWT

jwt_test_client creates GET and POST requests, adds valid JWT token to header and sends requests to:
- GET /services - to get a list of all services
- POST /service - to add a new service

To run test client:

```
python jwt_test_client.py 
```

## Data access

Two DAO objects - service_dao and user_dao - created with stub data to ensure that authentication and view use similar data as LIVE application.
User api_key created uniquely when new user account added into the system.

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