class Config(object):
    DEBUG = False
    AUTH_REQUIRED = True


class Development(Config):
    DEBUG = True
    AUTH_REQUIRED = True


class Test(Config):
    DEBUG = False
    AUTH_REQUIRED = True


configs = {
    'development': Development,
    'test': Test
}
