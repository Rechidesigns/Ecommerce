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
from core.validators import validate_phone_number
from store.choices import PAYMENT_PENDING, PAYMENT_STATUS, RATING_CHOICES, SHIPPING_STATUS_CHOICES, SHIPPING_STATUS_PENDING
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
    
    hex_code = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name = _("Hex Code"),
        help_text = _("This holds the hex color code of the colour name")
        )

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
        max_digits=8, decimal_places=2, 
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
    
    code = models.CharField(
        max_length=8, unique=True, 
        editable=False,
        verbose_name= _("Code"),
        help_text= _(" This holds the Coupon code of the product")
        )
    
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name= _("Price"),
        help_text= _(" This holds the Coupon price of the product")
        )
    
    expired = models.BooleanField(
        default =False,
        verbose_name= _("Expired"),
        help_text= _("This holds the code action if active or not")
        )
    
    expiry_date = models.DateTimeField(
        verbose_name= _("Expiry Date"),
        help_text= _(" This holds the expiry date of the code")
        )

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


class Order(BaseModel):
    
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, 
        null=True, related_name="orders",
        verbose_name = _("Customer Order"),
        help_text = _("This holds the CUSTOMER's order details")
        )
    
    transaction_ref = models.CharField(
        max_length=32, unique=True,
        verbose_name = _("Transaction Reference"),
        help_text = _("This holds the Transaction reference number of the order placed by the customer")
        )
    
    placed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name = _("Placed At"),
        help_text = _("This holds the time and date that the customer placed the order") 
        )
    
    total_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True,
        verbose_name = _("Total Price"),
        help_text = _("This holds the total price of the products orderd by the customer")
        )
    
    address = models.ForeignKey('Address',
        on_delete=models.SET_NULL, 
        blank=True, null=True,
        related_name="orders_address",
        verbose_name = _("Order Address"),
        help_text = _("This holds the address of the customer that placed the order")
        )
    
    payment_status = models.CharField(
        max_length=2, choices=PAYMENT_STATUS,
        default=PAYMENT_PENDING,
        verbose_name = _("Payment Status"),
        help_text = _("This holds the status of the payment of the order")
        )
    
    shipping_status = models.CharField(
        max_length=2, choices=SHIPPING_STATUS_CHOICES, 
        default=SHIPPING_STATUS_PENDING,
        verbose_name = _("Shipping Status"),
        help_text = _("This holds the Shipping status of the order placed by the customer")
        )

    def __str__(self):
        return f"{self.transaction_ref} --- {self.placed_at}"


class OrderItem(BaseModel):
    
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, 
        related_name="order_items", null=True,
        verbose_name = _("Customer"),
        help_text = _("This holds the the details of the customer that placed the order item")
        )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, 
        related_name="items",
        verbose_name = _("Orders"),
        help_text = _("This holds the the details of the order that was placed")
        )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="orderitems",
        verbose_name = _("Product Details"),
        help_text = _("This holds the details of the product that was ordered")
        )
    
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name = _("Quantity"),
        help_text = _("This holds the quantity of the order item that was placed")
        )
    
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name = _("Unit Price"),
        help_text = _("This holds the unit price of the order item that was placed")
        )
    
    size = models.CharField(
        max_length=20, null=True,
        verbose_name = _("Size"),
        help_text = _("This holds the size of the item that was orderd")
        )
    
    colour = models.CharField(
        max_length=20, null=True,
        verbose_name = _("Colour"),
        help_text = _("This holds the name of the colour")
        )
    
    ordered = models.BooleanField(
        default=False,
        verbose_name = _("Orderd"),
        help_text = _("This holds the action of the the order that was placed")
        )

    def __str__(self):
        return (
            f"{self.order.transaction_ref} --- {self.product.title} --- {self.quantity}"
        )


class Cart(BaseModel):
    
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        null=True, related_name="carts",
        verbose_name = _("Customer Detail"),
        help_text = _("This holds the cutomer details that owns the cart"))
    
    class Meta:
        verbose_name_plural = _("Carts")

    @property
    def total_price(self):
        cart_total = sum([item.total_price for item in self.items.all()])
        return cart_total


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, 
        related_name="items",
        verbose_name = _("Cart Item"),
        help_text = _("This holds the the cart item details")
        )
    
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name = _("Product Details"),
        help_text = _("This holds the details of the product in the cart")
        )
    
    size = models.CharField(
        max_length=20, null=True,
        verbose_name = _("Size"),
        help_text = _("This holds the size of the product or item in the cart")
        )
    
    colour = models.CharField(
        max_length=20, null=True,
        verbose_name = _("Colour Name"),
        help_text = _("This holds the name of the colour")
        )
    
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name = _("Colour Name"),
        help_text = _("This holds the name of the colour")
        )
    
    extra_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True,
        verbose_name = _("Extra Price"),
        help_text = _("This holds the extra price of the cart item")
        )

    @property
    def total_price(self):
        extra_price = self.extra_price
        if float(self.product.discount_price) > 0:
            return self.quantity * (
                self.product.discount_price + self.product.shipping_fee + extra_price
                )
        return self.quantity * (self.product.price + self.product.shipping_fee + extra_price)

    def __str__(self):
        return f"Cart id({self.cart.id}) ---- {self.product.title} ---- {self.quantity}"


class Country(BaseModel):
    
    name = models.CharField(
        max_length=255,
        verbose_name = _("Country Name"),
        help_text = _("This holds the name of the Country")
        )
    
    code = models.CharField(
        max_length=10,
        verbose_name = _("Code"),
        help_text = _("This holds the county code")
        )

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} -- {self.code}"


class Address(BaseModel):
    
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, 
        related_name="addresses",
        verbose_name = _("Customer"),
        help_text = _("This holds the customer details")
    )
    
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name = _("Country"),
        help_text = _("This holds the country details the customer address")
        )
    
    first_name = models.CharField(
        max_length=255,
        verbose_name = _("First Name"),
        help_text = _("This holds the first name of the customer")
        )
    
    last_name = models.CharField(
        max_length=255,
        verbose_name = _("Last Name"),
        help_text = _("This holds the name of the customer")
        )
    
    street_address = models.CharField(
        max_length=255,
        verbose_name = _("Street Address"),
        help_text = _("This holds the street aaddress of the customer")
        )
    
    second_street_address = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name = _("Second Street Address"),
        help_text = _("This holds the name of the second address of the customer")
        )
    
    city = models.CharField(
        max_length=255,
        verbose_name = _("City"),
        help_text = _("This holds the name of the city of the customer")
        )
    
    state = models.CharField(
        max_length=255,
        verbose_name = _("State"),
        help_text = _("This holds the name of the State of the customer")
        )
    
    zip_code = models.CharField(
        max_length=10,
        verbose_name = _("Zip Code"),
        help_text = _("This holds the zip code the customers address")
        )
    
    phone_number = models.CharField(
        max_length=20, validators=[validate_phone_number],
        verbose_name = _("Phone Number"),
        help_text = _("This holds the phone number of the customer")
        )

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.customer.full_name}"
