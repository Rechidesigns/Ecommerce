from django.shortcuts import get_object_or_404
# from rest_framework import rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView , ListAPIView , CreateAPIView
from store.models import (Product, Category, Size, Colour, 
                          ColourInventory, SizeInventory, ProductImage, 
                          ProductReview, ProductReviewImage, CouponCode, Order, OrderItem, 
                          Cart, CartItem, Country, Address)
from store.api.serializers import (ProductSerializer, CategorySerializer, SizeSerializer, ColourSerializer, 
                          ColourInventorySerializer, SizeInventorySerializer, ProductImageSerialer, 
                          ProductReviewSerializer, ProductReviewImageSerializers, CouponCodeSerializers, OrderSerializer, 
                          OrderItemSerializers, CartSerializer, CartItemSerializer, CountrySerializer,
                          AddressSerializer)

class CategoryView( ListCreateAPIView ):
    
    serializer_class = CategorySerializer
    permission_classes = [ IsAuthenticated, ]
    
    def post (self, request, *args, **kwargs):
        
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            serializer.save()
            
            return Response( {'status':'successful', 'message':'Category has been added successful','data':serializer.data} , status = status.HTTP_201_CREATED )

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def get (self, request, *args, **kwargs):
        
        qs = Category.objects.filter( )
        serializer = CategorySerializer(qs , many = True)
        return Response( {'status':'successful', 'message':'All categories has been fetched','data':serializer.data } , status=status.HTTP_200_OK )
    

class ProductView ( ListCreateAPIView ):
    
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,]
    
    def post (self, request, *args, **kwargs):
        
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save( )
            
            return Response( {'status':'successful', 'message':'Product has been added successful','data':serializer.data} , status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
                          
    def get ( self, request, *args, **kwargs):
        
        qs = Product.objects.all( )
        serializer = ProductSerializer(qs, data = request.data)
        return Response( {'status':'successful', 'message':'All products has been fetched','data':serializer.data } , status=status.HTTP_200_OK )
    
        
    

class ProductDetalView ( RetrieveUpdateDestroyAPIView ):
    
    serializer_class = ProductSerializer
    permission_classes = [ IsAuthenticated ]
    
    def get_object(self, product_id):
        
        product = get_object_or_404( Product, id = product_id )
        return product
    
    def get ( self, request, product_id):
        product = self.object(product_id)
        serializer = self.serializer_class(product)
        return Response({'status':'successful','message':'the detail information about the product','data':serializer.data }, status = status.HTTP_200_OK )

    def put ( self, request, product_id, format=None):
        product = self.get_object(product_id)
        serializer = ProductSerializer( product, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'successful', 'message':'the details of the product has been updated'}, status = status.HTTP_200_OK)
        return Response({'status':'fail'},serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, product_id, format=None):
        product = self.get_object(product_id)
        product.delete()
        return Response({'status':'successful','message':'the product has been deleted successful','data':[] }, status = status.HTTP_200_OK )
    
        

        
        
    