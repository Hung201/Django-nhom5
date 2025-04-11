from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import logging

# Create your views here.

@api_view(["GET"])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response({
        "DT": serializer.data,
        "EC": 0,
        "EM": "Get all products succeed"
    })

class ProductCreateView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Log request data for debugging
        logging.info(f"Request data: {request.data}")
        logging.info(f"Files in request: {request.FILES}")
        
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            # Trả về dữ liệu với URL ảnh đầy đủ
            return Response({
                "DT": serializer.data,
                "EC": 0,
                "EM": "Create product succeed"
            }, status=status.HTTP_201_CREATED)
        # Log validation errors
        logging.error(f"Validation errors: {serializer.errors}")
        return Response({
            "DT": None,
            "EC": 1,
            "EM": "Create product failed",
            "Errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        # Log request data for debugging
        logging.info(f"Update request data: {request.data}")
        logging.info(f"Files in update request: {request.FILES}")
        
        product_id = request.data.get("id")
        if not product_id:
            return Response({
                "DT": None,
                "EC": 1,
                "EM": "Product ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                "DT": None,
                "EC": 1,
                "EM": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_product = serializer.save()
            # Trả về dữ liệu với URL ảnh đầy đủ
            return Response({
                "DT": serializer.data,
                "EC": 0,
                "EM": "Update product succeed"
            }, status=status.HTTP_200_OK)

        # Log validation errors
        logging.error(f"Update validation errors: {serializer.errors}")
        return Response({
            "DT": None,
            "EC": 1,
            "EM": "Update product failed",
            "Errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({
                "DT": None,
                "EC": 1,
                "EM": "Product ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, context={'request': request})
            product_data = serializer.data
            product.delete()
            return Response({
                "DT": product_data,
                "EC": 0,
                "EM": "Delete product succeed"
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                "DT": None,
                "EC": 1,
                "EM": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)