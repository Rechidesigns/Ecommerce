from .settings import *
from decouple import config

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", False, cast=bool)

ALLOWED_HOSTS = [""]

CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    },
}

INSTALLED_APPS.remove("debug_toolbar")

MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

EMAIL_USE_TLS = True

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

EMAIL_PORT = 587
