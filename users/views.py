from .models import Company
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import CreateCompanySerializer, GetCompanySerializer, ListCompanySerializer, UserSerializer


class CompanyView(viewsets.ModelViewSet):
	filter_fields = ('industry')

	def perform_create(self, serializer):
		serializer.save(created_by_id=self.request.user.id)

	def get_serializer_class(self):
		serializer = self.request.query_params.get('serializer')
		if serializer == "create":
			return CreateCompanySerializer
		elif serializer == "get":
			return GetCompanySerializer
		return ListCompanySerializer

	def get_queryset(self):
		serializer = self.request.query_params.get('serializer')
		if serializer == "get":
			return Company.objects.select_related('created_by').prefetch_related('managed_by')
		return Company.objects.all()
	

class UserView(viewsets.ModelViewSet):

	def get_serializer_class(self):
		return UserSerializer

	def get_queryset(self):
		return User.objects.all()