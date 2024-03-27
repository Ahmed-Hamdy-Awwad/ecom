from rest_framework import routers
from django.urls import include, path
from .views import OrderViewSet, OrderItemViewSet


router = routers.DefaultRouter()
router.register("order", OrderViewSet, "order")
router.register("order-item", OrderItemViewSet, "order-item")
urlpatterns = [
	# path("", include(router.urls)),
	# path("yourpattern", yourview.as_view()),
]
