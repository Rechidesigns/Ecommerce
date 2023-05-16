from urllib.parse import urlencode

from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from store.forms import ProductAdminForm
from store.models import Category, Colour, ColourInventory, CouponCode, Product, ProductImage, Size, SizeInventory

# Register your models here.
admin.site.register((Size,))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "products_count",)
    list_filter = ("name",)
    ordering = ("name",)

    @admin.display(ordering="products_count")
    def products_count(self, category):
        url = (reverse("admin:store_product_changelist")
               + "?"
               + urlencode({"category__id": str(category.id)})
               )

        return format_html('<a href="{}">{} Products</a>', url, category.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))


@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code",)
    list_filter = ("name", "hex_code",)
    ordering = ("name",)
    search_fields = ("name", "hex_code",)


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<20", "Low")]

    def queryset(self, request, queryset):
        if self.value() == "<20":
            return queryset.filter(product_color_size_inventory__quantity__lt=20)


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 2
    max_num = 3


class SizeInventoryInline(admin.TabularInline):
    model = SizeInventory
    extra = 1


class ColourInventoryInline(admin.TabularInline):
    model = ColourInventory
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageAdmin, SizeInventoryInline, ColourInventoryInline)
    form = ProductAdminForm
    list_display = ("seller_name", "title", "category", "price", "percentage_off", "discount_price",
                    "average_ratings", "inventory", "inventory_status",)
    list_filter = ("category", "percentage_off", InventoryFilter)
    list_per_page = 30
    list_select_related = ("category",)
    ordering = ("title", "category", "percentage_off",)
    readonly_fields = ("product_images",)
    search_fields = ("title", "category__name",)

    @staticmethod
    def seller_name(obj: Product):
        return obj.seller.user.full_name

    @staticmethod
    def inventory_status(obj: Product):
        if obj.inventory < 10:
            return "Low"
        return "High"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
                request,
                f"{updated_count} products were successfully updated.",
                messages.ERROR,
        )

    @staticmethod
    def product_images(obj: Product):
        product_images = obj.images.all()
        html = ''
        for product in product_images:
            html += '<img src="{url}" width="{width}" height="{height}" />'.format(
                    url=product.image.url,
                    width=300,
                    height=200,
            )
        return mark_safe(html)


@admin.register(CouponCode)
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "price", "expired",)
    list_filter = ("expired", "price",)
    list_per_page = 20
    ordering = ("code", "expired",)
    search_fields = ("price",)
