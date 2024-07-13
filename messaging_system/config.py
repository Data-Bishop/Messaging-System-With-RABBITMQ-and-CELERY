class Config:
    # Celery Cofiguration
    CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'rpc://'

    # SMTP Configuration
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'nkanangabasifreke.data@gmail.com'  # Set this environment variable
    SMTP_PASSWORD = 'evxpptjrzitentsz'  # Set this environment variable
    LOG_FILE = '/var/log/messaging_system.log'
