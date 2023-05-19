from rest_framework import rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView , ListAPIView , CreateAPIView
from store.models import (Product, Category, Size, Colour, 
                          ColourInventory, SizeInventory, ProductImage, 
                          ProductReview, ProductReviewImage, CouponCode, Order, OrderItem, 
                          Cart, CartItem, Country, Address)
from store.serializers import (ProductSerializer, CategorySerializer, SizeSerializer, ColourSerializer, 
                          ColourInventorySerializer, SizeInventorySerializer, ProductImageSerialer, 
                          ProductReviewSerializer, ProductReviewImageSerializers, CouponCodeSerializers, OrderSerializer, 
                          OrderItemSerializers, CartSerializer, CartItemSerializer, CountrySerializer,
                          AddressSerializer)

class CategoryView(APIView):
    
    serializer_class = CategorySerializer
    # permission_classes = [ AllowAny, ]
    
    def post (self, request, *args, **kwargs):
        
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            serializer.save()
            
            return Response( {'status':'successful', 'message':'Category has been added successful','data':serializer.data} , status = status.HTTP_201_CREATED )

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def get (self, request, *args, **kwargs):
        
        qs = Category.objects.filter( )
        serializer = CategorySerializer(qs , many = True)
        return Response( {'status':'successful', 'message':'All categories has been fetched','data':serializer.data } , status=status.HTTP_201_CREATED )
    

    