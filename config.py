class Config:
    """Contains config settings for general application"""

    APP = "app"
    ENV = "development"
    TESTING = True
    DEBUG = True
    MONGO_URI = (
        "mongodb+srv://jahstudiosapps:1OP8AhNla2ge3q5K@testenv.jzp9lnr.mongodb.net/lemonaid?retryWrites=true&w=majority"
    )
    MONGO_HOST = "mongodb+srv://testenv.jzp9lnr.mongodb.net"
    MONGO_DB = "lemonaid"
    MONGO_USER = "jahstudiosapps"
    MONGO_PASSWORD = "1OP8AhNla2ge3q5K"
    SECRECT_KEY = "mysecrets"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 604800
