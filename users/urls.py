from .views import CompanyView
from rest_framework import routers
from django.urls import include, path


router = routers.DefaultRouter()
router.register("company", CompanyView, "company")
urlpatterns = [
	path("", include(router.urls)),
	# path("yourpattern", yourview.as_view()),
]
