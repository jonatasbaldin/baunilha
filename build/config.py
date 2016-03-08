class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
