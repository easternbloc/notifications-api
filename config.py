import os


class Config(object):
    DEBUG = False
    NOTIFY_LOG_LEVEL = 'DEBUG'
    NOTIFY_APP_NAME = 'api'
    NOTIFY_LOG_PATH = '/var/log/notify/application.log'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/notification_api'
    NOTIFY_DATA_API_URL = os.getenv('NOTIFY_API_URL', "http://localhost:6001")
    NOTIFY_DATA_API_AUTH_TOKEN = os.getenv('NOTIFY_API_TOKEN', "dev-token")
    ADMIN_CLIENT_USER_NAME = None
    ADMIN_CLIENT_SECRET = None


class Development(Config):
    DEBUG = True
    SECRET_KEY = 'secret-key'
    DANGEROUS_SALT = 'dangerous-salt'
    ADMIN_CLIENT_USER_NAME = 'dev-notify-admin'
    ADMIN_CLIENT_SECRET = 'dev-notify-secret-key'


class Test(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_notification_api'
    SECRET_KEY = 'secret-key'
    DANGEROUS_SALT = 'dangerous-salt'
    ADMIN_CLIENT_USER_NAME = 'dev-notify-admin'
    ADMIN_CLIENT_SECRET = 'dev-notify-secret-key'


class Live(Config):
    pass


configs = {
    'development': Development,
    'test': Test,
    'live': Live,
}
