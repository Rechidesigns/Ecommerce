import secrets

from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
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
    
    name = models.CharField(
        max_length=255,
        verbose_name = _("Category Name"),
        help_text =_("This holds the name of the category")
        )

    def __str__(self):
        return str(self.name)


class Size(BaseModel):
    
    title = models.CharField(
        max_length=5, 
        unique=True,
        verbose_name= _("Size"),
        help_text = _("This holds the size of the product")
        )

    def __str__(self):
        return str(self.title)


class Colour(BaseModel):
    
    name = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name = _("Colour Name"),
        help_text = _("This holds the name of the colour")
        )
    
    hex_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ---- {self.hex_code}"


class ProductsManager(models.Manager):
    def get_queryset(self):
        return super(ProductsManager,
                     self).get_queryset().prefetch_related(
                         'category', 'product_reviews',
                        'size_inventory', 'color_inventory',
                        'images').filter(inventory__gt=0)


class Product(BaseModel):
    
    seller = models.ForeignKey(
        Seller, null=True,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Seller"),
        help_text= _("This holds the owner or seller of the product (user)")
        )
        
    title = models.CharField(
        max_length=255, 
        unique=True, null=True,
        verbose_name= _("Title"),
        help_text= _("This holds the title of the product")
        )
    
    slug = AutoSlugField(
        populate_from="title", 
        unique=True, always_update=True, 
        editable=False, null=True,
        verbose_name= _("Slug"),
        help_text= _(" This holds the slug of the product")
        )
    
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name="products", null=True,
        verbose_name= _("Category"),
        help_text= _("This holds the category the product belongs to")
        )
    
    description = models.TextField(
        null=True, blank= True,
        verbose_name= _("Description"),
        help_text= _("This holds the description of the product")
        )
    
    style = models.CharField(
        max_length=255, null=True,
        verbose_name= _("Style"),
        help_text= _("This holds the style of the product")
        )
    
    price = models.DecimalField(
        max_digits=6, decimal_places=2, 
        default=0, 
        verbose_name= _("Price"),
        help_text= _("This holds the price or amount of the product")
        )
    
    shipping_out_days = models.IntegerField(
        default=0,
        verbose_name= _("Shipping Out Days"),
        help_text= _(" This holds the shipping days of the product")
        )
    
    shipping_fee = models.DecimalField(
        max_digits=6, decimal_places=2, 
        validators=[MinValueValidator(0)], default=0,
        verbose_name= _("Shipping Fee"),
        help_text= _(" This holds the shipping fee of the product")
        )
    
    inventory = models.IntegerField(
        validators=[MinValueValidator(0)], null=True,
        verbose_name= _("Inventory"),
        help_text= _(" This holds the inventory details of the product")
        )
    
    percentage_off = models.PositiveIntegerField(
        default=0,
        verbose_name= _("Percentage Off"),
        help_text= _(" This holds the percentage of the product will be sold off"))
    
    flash_sale_start_date = models.DateTimeField(
        null=True, blank=True,
        verbose_name= _("Flashsale Start Date"),
        help_text= _(" This holds the flashsale start date of the product")
        )
    
    flash_sale_end_date = models.DateTimeField(
        null=True, blank=True,
        verbose_name= _("Flashsale End Date"),
        help_text= _(" This holds the flashsale end date of the product")
        )
    
    featured_product = models.BooleanField(
        default=False,
        verbose_name= _("Featured Product"),
        help_text= _(" This holds the featured product")
        )
    
    
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
    
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="color_inventory",
        verbose_name= _("Product Detail"),
        help_text= _(" This holds the product that has the colour")
        )
    
    colour = models.ForeignKey(
        Colour, on_delete=models.CASCADE,
        related_name="product_color",
        verbose_name= _("Product Colour"),
        help_text= _(" This holds the color of the product")
        )
    
    quantity = models.IntegerField(
        default=0, blank=True,
        verbose_name= _("Quantity"),
        help_text= _(" This holds the quantity of the product")
        )
    
    extra_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True, default=0,
        verbose_name= _("Extra Price"),
        help_text= _(" This holds the Extra Price given to the product")
        )

    class Meta:
        verbose_name_plural = "Product Color & Inventories"

    def __str__(self):
        return self.product.title


class SizeInventory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="size_inventory",
        verbose_name= _("Product Detail"),
        help_text= _(" This holds the detail of the product")
        )
    
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, 
        related_name="product_size",
        verbose_name= _("Product Size"),
        help_text= _(" This holds the size of the product")
        )
    
    quantity = models.IntegerField(
        default=0, blank=True,
        verbose_name= _("Quantity"),
        help_text= _(" This holds the quantity of the product")
        )
    
    extra_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True, default=0,
        verbose_name= _("Extra Price"),
        help_text= _(" This holds the extra price of the product")
        )

    class Meta:
        verbose_name_plural = "Product Size & Inventories"

    def __str__(self):
        return self.product.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="images",
        verbose_name= _("Product Details"),
        help_text= _(" This holds the Id or details of the product that owns the image")
        )
    
    _image = models.ImageField(
        upload_to='store/images',
        validators=[validate_image_size],
        verbose_name= _("Image"),
        help_text= _(" This holds the image of the product")
        )

    def __str__(self):
        return self.product.title

    @property
    def review_image(self):
        if self._image is not None:
            return self._image.url
        return None


class ProductReview(BaseModel):
    
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING,
        related_name="product_reviews",
        verbose_name= _("Customer"),
        help_text= _(" This holds the customer details that owns the review of the product")
        )
    
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="product_reviews",
        verbose_name= _("Product Details"),
        help_text= _(" This holds the details of the product on review")
        )
    
    ratings = models.IntegerField(
        choices=RATING_CHOICES, null=True,
        verbose_name= _("Rating"),
        help_text= _(" This holds the rating of the product")
        )
    
    description = models.TextField(
        verbose_name= _("Description"),
        help_text= _(" This holds the descriptions of review the product has")
    )

    def __str__(self):
        return f"{self.customer.user.full_name} --- {self.product.title} --- {self.ratings} stars"


class ProductReviewImage(models.Model):
    
    product_review = models.ForeignKey(
        ProductReview, on_delete=models.CASCADE, 
        related_name="product_review_images",
        verbose_name= _("Product Review Image"),
        help_text= _(" This holds the product the image belongs to")
        )
    _image = models.ImageField(
        upload_to="store/product_reviews", 
        validators=[validate_image_size],
        verbose_name= _("Image"),
        help_text= _(" This holds the image of the product on review")
        )

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
