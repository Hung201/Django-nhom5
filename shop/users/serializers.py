from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()  # Lấy model user theo settings.AUTH_USER_MODEL

class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'image']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'image']

    def create(self, validated_data):
        image = validated_data.pop('image', None)  # Tránh lỗi nếu không có ảnh
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_staff=validated_data.get('is_staff', False)  # Mặc định False
        )
        if image:
            user.image = image
            user.save()
        return user
    


class UserUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['email', 'is_staff', 'image']  # Chỉ cho phép update 3 trường

    def update(self, instance, validated_data):
        # Cập nhật email
        instance.email = validated_data.get('email', instance.email)

        # Cập nhật is_staff (nếu có)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)

        # Cập nhật ảnh nếu có
        image = validated_data.get('image', None)
        if image:
            instance.image = image

        instance.save()
        return instance