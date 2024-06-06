from rest_framework import routers
from django.urls import include, path
from .views import ocr_process


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("process/", ocr_process, name="process"),
]
