from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, ProductPriceViewSet
from rest_framework import routers

# urlpatterns = [
#     path('category/<int:pk>/', CategoryAPIView.as_view(), name="category"),
#     path('category/', CategoryAPIView.as_view(), name="categories"),
#     path('product/<int:pk>/', ProductAPIView.as_view(), name="product"),
#     path('product/', ProductAPIView.as_view(), name="products"),
# ]

router = routers.DefaultRouter()
router.register("category", CategoryViewSet, "category")
router.register("product", ProductViewSet, "product")
router.register("product-prices", ProductPriceViewSet, "product-prices")

urlpatterns = [
    path("", include(router.urls)),
#     path('category/<int:pk>/', CategoryAPIView.as_view(), name="category"),
#     path('category/', CategoryAPIView.as_view(), name="categories"),
#     path('product/<int:pk>/', ProductAPIView.as_view(), name="product"),
#     path('product/', ProductAPIView.as_view(), name="products"),
]