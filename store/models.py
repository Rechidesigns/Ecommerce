from django.db import models
from common.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from locations.models import Country


class Category(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Category name'),
        help_text=_('product category name')
        )
    
    created_date = models.DateTimeField(
        default=timezone.now,
        blank=True, editable=False,
        verbose_name=_('Created Date'),
        help_text=_('Timestamp when the category was created')
        )
    
    
    def __str__(self):
        return str(self.name)
    

class Product(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        verbose_name = _('product category name'),
        related_name = "Product_category",
        null = True,
        help_text=_(' This is a product category')
    )
    
    name = models.CharField(
        verbose_name= _('Product name'),
        max_length= 255,
        null = True,
        help_text=_('This holds the name of the product')
    )
    
    product_description = models.CharField(
        verbose_name = _('Product description'),
        max_length = 500,
        null = True,
        blank = True,
        help_text = _('This holds the description of the product')
    )
    
    price = models.DecimalField(
        verbose_name = _('Product price'),
        null=True, blank=True,
        max_digits = 300, 
        decimal_places = 2,
        default=0.00,
        help_text=_("This holds the price of the product")
    )
    
    product_image = models.ImageField(
        verbose_name = _('Product Image'),
        upload_to = "photos/product_image",
        null =True,
        blank=True,
        help_text= _('Product images, which should be in PNG, JPEG, or JPG format')
    )
    
    def __str__(self):
        return self.name
    
    

class PropertyImage (BaseModel):
    # adding product multiple images
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True,
        verbose_name=_("Product"),
        help_text=_("Product of which the images belongs to.")
    )

    image = models.ImageField(
        verbose_name = _('Product Image'),
        upload_to = "photos/properties_image",
        null =True,
        help_text= _('Product images, which should be in PNG, JPEG, or JPG format')
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return str(self.product)
    
    
