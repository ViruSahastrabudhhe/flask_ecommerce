class Config():
    DEBUG=True

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    pass

configuration = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}