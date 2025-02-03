
class Config:
    SECRET_KEY = "SECRET_KEY"
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    # tls is 587, ssl is 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "mygmail"
    MAIL_PASSWORD = "mycode"