from django.urls import path
from . import views

urlpatterns = [
    path("api/products", views.products, name="products"),
    path("api/products/create", views.ProductCreateView.as_view(), name="create-product"),
    path("api/products/update", views.ProductUpdateView.as_view(), name="update-product"),
    path("api/products/delete", views.ProductDeleteView.as_view(), name="delete-product"),
]
