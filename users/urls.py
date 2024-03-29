from .views import *
from rest_framework import routers
from django.urls import include, path


router = routers.DefaultRouter()
router.register("user", UserView, "user")
router.register("company", CompanyView, "company")
router.register("document", DocumentView, "document")
urlpatterns = [
	path("", include(router.urls)),
	# path("yourpattern", yourview.as_view()),
]
