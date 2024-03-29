from rest_framework import routers
from django.urls import include, path
from .views import CompanyView, UserView


router = routers.DefaultRouter()
router.register("user", UserView, "user")
router.register("company", CompanyView, "company")
urlpatterns = [
	path("", include(router.urls)),
	# path("yourpattern", yourview.as_view()),
]
