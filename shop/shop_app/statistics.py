from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["GET"])
def overview_statistics(request):
    try:
        # Đếm tổng số sản phẩm
        total_products = Product.objects.count()

        # Đếm số user theo is_staff
        staff_users = User.objects.filter(is_staff=True).count()
        normal_users = User.objects.filter(is_staff=False).count()

        # Đếm số brand (không tính các brand là null)
        total_brands = Product.objects.values('brand').exclude(brand__isnull=True).distinct().count()

        return Response({
            "DT": {
                "total_products": total_products,
                "total_staff_users": staff_users,
                "total_normal_users": normal_users,
                "total_brands": total_brands
            },
            "EC": 0,
            "EM": "Get overview statistics succeed"
        })
    except Exception as e:
        return Response({
            "DT": None,
            "EC": 1,
            "EM": f"Error getting statistics: {str(e)}"
        }) 