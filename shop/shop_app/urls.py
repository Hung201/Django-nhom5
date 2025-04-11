from django.urls import path
from . import views
from . import statistics

urlpatterns = [
    path("api/products", views.products, name="products"),
    path("api/products/create", views.ProductCreateView.as_view(), name="create-product"),
    path("api/products/update", views.ProductUpdateView.as_view(), name="update-product"),
    path("api/products/delete", views.ProductDeleteView.as_view(), name="delete-product"),
    path("api/overview-statistics", statistics.overview_statistics, name="overview-statistics"),
]
