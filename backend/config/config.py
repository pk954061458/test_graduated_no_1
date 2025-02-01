class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/tourism'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 