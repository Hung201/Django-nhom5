from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from .serializers import UserUpdateSerializer
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()  # Lấy model user theo settings.AUTH_USER_MODEL


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Cho phép tất cả truy cập API này  

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response({
            "DT": serializer.data,
            "EC": 0,
            "EM": "GetAll list participants succeed"
        })

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
        

class UserDeleteView(APIView):

    def delete(self, request):
        # Lấy user_id từ body của yêu cầu (x-www-form-urlencoded)
        user_id = request.data.get('user_id')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                return Response({
                    "DT": {"id": user_id},
                    "EC": 0,
                    "EM": "Delete the user succeed"
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    "DT": None,
                    "EC": 1,
                    "EM": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "DT": None,
                "EC": 1,
                "EM": "user_id parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        

class UserUpdateView(APIView):
    permission_classes = [AllowAny]  # API có thể được gọi mà không cần token
    parser_classes = [MultiPartParser, FormParser]  # Hỗ trợ upload file ảnh

    def put(self, request):
        user_id = request.data.get("id")  # Lấy id từ request body
        if not user_id:
            return Response({
                "DT": None,
                "EC": 1,
                "EM": "User ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "DT": None,
                "EC": 1,
                "EM": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "DT": {
                    "id": user.id,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "image": user.image.url if user.image else None
                },
                "EC": 0,
                "EM": "Update the user succeed"
            }, status=status.HTTP_200_OK)

        return Response({
            "DT": None,
            "EC": 1,
            "EM": "Update failed",
            "Errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)