from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

from common.models import BaseModel
from core.choices import GENDER_CHOICES
from core.validators import validate_full_name, validate_phone_number
from .managers import CustomUserManager


# Create your models here


def upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/customer/instance_id/<filename>
    return f"users/{instance.id[:5]}/{filename}"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    username = None
    full_name = models.CharField(max_length=255, validators=[validate_full_name])
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    country = CountryField()
    address = models.CharField(max_length=255)
    _profile_picture = models.ImageField(upload_to=upload_path)
    email_changed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    @property
    def profile_picture(self):
        if self._profile_picture is not None:
            return self._profile_picture.url
        return None


class Seller(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller")
    company_name = models.CharField(max_length=255)
    ratings = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user.full_name} -- User {self.user.email}"


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)

    def __str__(self):
        return f"{self.user.full_name} -- User {self.user.email}"


class Otp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp")
    code = models.PositiveIntegerField(null=True)
    expired = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.user.full_name} ----- {self.code}"

    def save(self, *args, **kwargs):
        self.expiry_date += timezone.timedelta(minutes=15)
        if timezone.now() == self.expiry_date:
            self.expired = True
            self.delete()
        super(Otp, self).save(*args, **kwargs)
