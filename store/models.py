import secrets

from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.functional import cached_property
from rest_framework.exceptions import ValidationError

from common.models import BaseModel
from core.models import Customer, Seller
from store.choices import RATING_CHOICES
from store.validators import validate_image_size


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Size(BaseModel):
    title = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return str(self.title)


class Colour(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    hex_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ---- {self.hex_code}"


class ProductsManager(models.Manager):
    def get_queryset(self):
        return super(ProductsManager, self).get_queryset().prefetch_related('category', 'product_reviews',
                                                                            'size_inventory', 'color_inventory',
                                                                            'images').filter(inventory__gt=0)


class Product(BaseModel):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="products", null=True)
    title = models.CharField(max_length=255, unique=True, null=True)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True, editable=False, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True)
    description = models.TextField(null=True)
    style = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shipping_out_days = models.IntegerField(default=0)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    inventory = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    percentage_off = models.PositiveIntegerField(default=0)
    flash_sale_start_date = models.DateTimeField(null=True, blank=True)
    flash_sale_end_date = models.DateTimeField(null=True, blank=True)
    featured_product = models.BooleanField(default=False)
    objects = models.Manager()
    categorized = ProductsManager()

    def __str__(self):
        return f"{self.title} --- {self.category}"

    @cached_property
    def average_ratings(self):
        result = self.product_reviews.aggregate(Avg("ratings"))
        return result["ratings__avg"] or 0

    @property
    def discount_price(self):
        if self.percentage_off > 0:
            discount = self.price - (self.price * self.percentage_off / 100)
            return round(discount, 2)
        return 0


class ColourInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="color_inventory")
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, related_name="product_color")
    quantity = models.IntegerField(default=0, blank=True)
    extra_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0)

    class Meta:
        verbose_name_plural = "Product Color & Inventories"

    def __str__(self):
        return self.product.title


class SizeInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="size_inventory")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="product_size")
    quantity = models.IntegerField(default=0, blank=True)
    extra_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0)

    class Meta:
        verbose_name_plural = "Product Size & Inventories"

    def __str__(self):
        return self.product.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    _image = models.ImageField(upload_to='store/images', validators=[validate_image_size])

    def __str__(self):
        return self.product.title

    @property
    def review_image(self):
        if self._image is not None:
            return self._image.url
        return None


class ProductReview(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="product_reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_reviews")
    ratings = models.IntegerField(choices=RATING_CHOICES, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.customer.user.full_name} --- {self.product.title} --- {self.ratings} stars"


class ProductReviewImage(models.Model):
    product_review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name="product_review_images")
    _image = models.ImageField(upload_to="store/product_reviews", validators=[validate_image_size])

    @property
    def review_image(self):
        if self._image is not None:
            return self._image.url
        return None


class CouponCode(BaseModel):
    code = models.CharField(max_length=8, unique=True, editable=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    expired = models.BooleanField(default=False)
    expiry_date = models.DateTimeField()  #

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_hex(4).upper()  # creates 8 letters

        if self.expiry_date and timezone.now() > self.expiry_date:
            self.expired = True

        # ensure expiry date is always in the future
        if self.expiry_date < timezone.now():
            raise ValidationError('Expiry date must be in the future.')
        super().save(*args, **kwargs)
