class Config(object):
    DEBUG = False

    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/notify'


class Development(Config):
    DEBUG = True


class Test(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_notifications_api'


configs = {
    'development': Development,
    'test': Test
}
