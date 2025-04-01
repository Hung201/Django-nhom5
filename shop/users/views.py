from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()  # Lấy model user theo settings.AUTH_USER_MODEL

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        # Kiểm tra nếu username hoặc password rỗng
        if not username or not password:
            return Response(
                {
                    "DT": "",
                    "EC": -3,
                    "EM": "Invalid Input Email/Password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kiểm tra xem user có tồn tại trong hệ thống không
        if not User.objects.filter(username=username).exists():
            return Response(
                {
                    "DT": "",
                    "EC": -1,
                    "EM": f"Not found user with the email: {username}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Xác thực tài khoản
        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {
                    "DT": "",
                    "EC": -3,
                    "EM": "Invalid Input Email/Password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Đăng nhập thành công, tạo hoặc lấy token
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                "username": user.username,
                "email": user.email,
                'is_staff':user.is_staff,
                "EC": 0,
                "EM": "Login succeed!"
            },
            status=status.HTTP_200_OK
        )
        
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

    
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': False,
                "EC": 0,
                "EM": "Register succeed!"
                    }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "EC": -1,
                "EM": "Register failed!"
                    }, status=status.HTTP_400_BAD_REQUEST)