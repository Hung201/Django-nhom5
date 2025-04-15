from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()  # Lấy model user theo settings.AUTH_USER_MODEL

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'image']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    image = serializers.ImageField(required=False, allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    is_staff = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'image', 
                 'first_name', 'last_name', 'city', 'state', 'address', 'phone']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
            'is_staff': {'default': False},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        try:
            # Đảm bảo is_staff luôn là False
            validated_data['is_staff'] = False
            
            image = validated_data.pop('image', None)
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password'],
                is_staff=False,  # Luôn set là False
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                city=validated_data.get('city', ''),
                state=validated_data.get('state', ''),
                address=validated_data.get('address', ''),
                phone=validated_data.get('phone', '')
            )
            if image:
                user.image = image
                user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))
    


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