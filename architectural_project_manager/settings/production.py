from architectural_project_manager.settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": int(config("POSTGRES_DB_PORT")),
    }
}
