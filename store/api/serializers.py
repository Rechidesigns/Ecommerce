from rest_framework import serializers
# from ecommerce.store.models import Size
from store.models import (Product, Category, Size, Colour, 
                          ColourInventory, SizeInventory, ProductImage, 
                          ProductReview, ProductReviewImage, CouponCode, Order, OrderItem, 
                          Cart, CartItem, Country, Address)


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        filds = ['seller', 'title', 'slug', 'category', 
                 'style', 'price', 'shipping_out_days', 
                 'shipping_fee', 'inventory', 'percentage_off', 
                 'flash_sale_start_date', 'flash_sale_end_date',
                 'featured_product', ]
        
        
class CategorySerializer(serializers.ModelSerializer):
    product =  ProductSerializer ( many=True, read_only=True )
    
    class Meta:
        model = Category
        fields = ['name','product',]
        
        
class SizeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Size
        fields = ['title',]
        
    
class ColourSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Colour
        fields = ['name', 'hex',]
        

class ColourInventorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ColourInventory
        fields = ['product', 'colour', 'quantity', 'extra_price', ]
        

class SizeInventorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SizeInventory
        fields = ['product', 'size', 'quantity','extra_price',]
        
        
class ProductImageSerialer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = ['product', '-image', 'ratings','description',]
        
        
class  ProductReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductReview
        fields = ['customer', 'product', 'ratings', 'description',]
        
        
        
class ProductReviewImageSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = ProductReviewImage
        fields = ['product_review', '-image',]
        

class CouponCodeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = CouponCode
        fields = ['code', 'price','expired', 'expiry_date',]
        
        
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['customer', 'transaction_ref', 'placed_at', 
                  'total_price', 'address', 'payment_status',
                  'shipping_status',]
        

class OrderItemSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['customer','order', 'product','quantity', 
                  'unit_price', 'size','colour','ordered',]
        
        
class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = ['customer',]
        

class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['cart','product','size','colour','quantity', 'extra_price',]
        
        
class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = ['name', 'code', ]
        
        
class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['customer', 'country', 'first_name', 'last_name', 
                  'street_address', 'second_street_address',
                  'city', 'state', 'zip_code', 'phone_number',]
        