class Config(object):
    DEBUG = True
    AUTH_REQUIRED = True


class Development(Config):
    DEBUG = True
    AUTH_REQUIRED = True


class Test(Config):
    DEBUG = True
    AUTH_REQUIRED = True


configs = {
    'development': Development,
    'test': Test
}
