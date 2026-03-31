import os

class Config:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("EMAIL_ADDRESS")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER="luzie.ahrens@gmail.com"
    MAIL_TIMEOUT = 5