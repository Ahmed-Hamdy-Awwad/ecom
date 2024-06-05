from django.urls import path
from .views import CategoryAPIView, ProductAPIView

urlpatterns = [
    path('category/<int:pk>/', CategoryAPIView.as_view(), name="category"),
    path('category/', CategoryAPIView.as_view(), name="categories"),
    path('product/<int:pk>/', ProductAPIView.as_view(), name="product"),
    path('product/', ProductAPIView.as_view(), name="products"),
]
