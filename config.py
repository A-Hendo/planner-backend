class Config:
    """Contains config settings for general application"""

    APP = "app"
    ENV = "development"
    TESTING = True
    DEBUG = True
    MONGO_URI = (
        "mongodb+srv://admin_ulster:password_ulster@cluster0.v2yzyt6.mongodb.net/com661_db?retryWrites=true&w=majority"  # noqa: E501
    )
    SECRECT_KEY = "mysecrets"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 604800
