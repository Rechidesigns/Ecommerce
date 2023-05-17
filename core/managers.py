from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    @staticmethod
    def email_validator(email):
        """
        Email Validator
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("You must provide a valid email address")

    def create_user(self, username, email, full_name, password, **extra_fields):
        """
        Create and save a user with the given username, full_name, email and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not full_name:
            raise ValueError("Full name is required")
        if not email:
            raise ValueError("Email address is required")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
                self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(email=email, username=username, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, full_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("Email address is required")
        
        return self.create_user(email, username, password, full_name, **extra_fields)
