from rest_framework import serializers
from .models import Product
import logging
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.request import Request

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        model = Product
        fields = ["id", "name", "sku", "image", "description", "brand", "price", "color"]
        read_only_fields = ['sku']  # SKU sẽ được tự động tạo

    def create(self, validated_data):
        image = validated_data.pop('image', None)  # Tránh lỗi nếu không có ảnh
        product = Product.objects.create(**validated_data)
        if image:
            product.image = image
            product.save()
            logging.info(f"Image saved: {product.image.url}")
        return product

    def update(self, instance, validated_data):
        # Cập nhật các trường khác
        for attr, value in validated_data.items():
            if attr != 'image':
                setattr(instance, attr, value)
        
        # Cập nhật ảnh nếu có
        image = validated_data.get('image', None)
        if image:
            instance.image = image
            logging.info(f"Image updated: {instance.image.url}")
        
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            # Lấy request từ context
            request = self.context.get('request')
            if request and isinstance(request, Request):
                # Lấy domain từ request
                domain = request.build_absolute_uri('/').rstrip('/')
                # Tạo URL đầy đủ
                representation['image'] = f"{domain}{instance.image.url}"
                logging.info(f"Full image URL: {representation['image']}")
            else:
                # Nếu không có request, sử dụng MEDIA_URL
                representation['image'] = instance.image.url
        return representation