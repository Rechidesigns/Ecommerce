"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.1.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z)v)lr$iebchs3zr8da%!k@7m4h=z%lp^r36kuk75ck#k)t_us"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', " "]

# Application definition

DJANGO_APPS = [
    "jazzmin",  # ADMIN..do not delete
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "common",
    "core",
    "store",
]

THIRD_PARTY_APPS = [
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "debug_toolbar",
    "cloudinary",
    "cloudinary_storage",
    "corsheaders",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 30,
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "NON_FIELD_ERRORS_KEY": "message",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "E-COMMERCE API",
    "DESCRIPTION": "A E-commerce API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "DISABLE_ERRORS_AND_WARNINGS": True,
}

INTERNAL_IPS = [
    "127.0.0.1",
]

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=15),
}

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "commerce.sqlite3",
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ecommerce_new',
#         'USER': 'postgres',
#         'PASSWORD': 'Alexwhite96',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "core.User"

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]

STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}




MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "static/media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"  # using terminal to receive email
)

# Gmail settings for development
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#
# EMAIL_USE_SSL = True
#
# EMAIL_HOST = "smtp.gmail.com"
#
# EMAIL_HOST_USER = "<email_address>"
#
# EMAIL_HOST_PASSWORD = "<email_address_app_password>"
#
# EMAIL_PORT = 465
#
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# JAZZMIN
# JAZZMIN_UI_TWEAKS = {
#     "theme": "minty",
#     "body_small_text": False,
#     # "theme": "darkly",
# }

# # JAZZMIN CONFIG
# JAZZMIN_SETTINGS = {
#     "site_brand": "E-COMMERCE ADMIN",
#     # title of the window (Will default to current_admin_site.site_title if absent or None)
#     "site_title": "E-COMMERCE ADMIN",
#     # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_header": "E-COMMERCE",
#     # Logo to use for your site, must be present in static files, used for brand on top left
#     "site_logo": "",
#     # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
#     "login_logo": "",
#     # CSS classes that are applied to the logo above
#     "site_logo_classes": "img-circle",
#     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
#     "site_icon": None,
#     # Welcome text on the login screen
#     "welcome_sign": "Welcome to the E-commerce Admin Section",
#     # Copyright on the footer
#     "copyright": "E-COMMERCE Ltd",
#     # The model admin to search from the search bar, search bar omitted if excluded
#     "search_model": "store.Product",
#     # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
#     "user_avatar": "avatar",
#     ############
#     # Top Menu #
#     ############
#     # Links to put along the top menu
#     "topmenu_links": [
#         # Url that gets reversed (Permissions can be added)
#         {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
#         # model admin to link to (Permissions checked against model)
#         # {"model": "accounts.User"},
#         # App with dropdown menu to all its models pages (Permissions checked against models)
#         {"app": "core"},
#         {"app": "store"},
#     ],
#     #############
#     # User Menu #
#     #############
#     # Additional links to include in the user menu on the top right ("app" url type is not allowed)
#     "usermenu_links": [{"name": "E-COMMERCE Platform"}, {"model": "auth.user"}],
#     #############
#     # Side Menu #
#     #############
#     # Whether to display the side menu
#     "show_sidebar": True,
#     # Whether to aut expand the menu
#     "navigation_expanded": True,
#     # Hide these apps when generating side menu e.g (auth)
#     "hide_apps": [],
#     # Hide these models when generating side menu (e.g auth.user)
#     "hide_models": [],
#     # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
#     "order_with_respect_to": ["auth", "core", "core.user", "core.customer", "core.seller" "store.product"],
#     # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
#     # for the full list of 5.13.0 free icon classes
#     "icons": {
#         "auth.group": "fas fa-users",
#         "authtoken.token": "fas fa-key",
#         "core.user": "fas fa-user",
#         "core.otp": "fas fa-circle-9",
#         "core.customer": "fas fa-user",
#         "core.seller": "fas fa-user",
#         "store.category": "fas fa-list-ul",
#         "store.colour": "fas fa-palette",
#         "store.couponcode": "fas fa-circle-9",
#         "store.product": "fas fa-shopping-basket",
#         "store.productimage": "fas fa-file-image",
#         "store.productreview": "fas fa-star",
#         "store.size": "fas fa-expand",
#     },
#     # Icons that are used when one is not manually specified
#     "default_icon_parents": "fas fa-chevron-circle-right",
#     "default_icon_children": "fas fa-circle",
#     #############
#     # UI Tweaks #
#     #############
#     "show_ui_builder": True,
#     "changeform_format": "horizontal_tabs",
#     # override change forms on a per modeladmin basis
#     "changeform_format_overrides": {
#         "auth.user": "collapsible",
#         "auth.group": "vertical_tabs",
#     },
# }


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": " Recuity Estate Project Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Welcome to Recuity Estate Project",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand":  " Recuity Estate Project",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Recuity Estate Project admin",

    # Copyright on the footer
    "copyright":  "Recuity Estate Project Library Ltd",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "auth.User",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages", 
            "url": "make_messages", 
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": True,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "materia",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False
}
