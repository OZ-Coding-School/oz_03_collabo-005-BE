from .local import *

# Static 파일의 경로 지정
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.joinpath("static")

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS_PROD").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST_PROD"),
        "NAME": os.environ.get("DB_NAME_PROD"),
        "USER": os.environ.get("DB_USER_PROD"),
        "PASSWORD": os.environ.get("DB_PASSWORD_PROD"),
        "PORT": os.environ.get("DB_PORT_PROD"),
    }
}
