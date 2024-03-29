from .serializers import *
from rest_framework import viewsets
from .models import Company, Document
from django.contrib.auth.models import User


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
	

class DocumentView(viewsets.ModelViewSet):

	def perform_create(self, serializer):
		serializer.save(created_by_id=self.request.user.id)

	def get_serializer_class(self):
		serializer = self.request.query_params.get('serializer')
		if serializer == "create":
			return CreateDocumentSerializer
		elif serializer == "get":
			return GetDocumentSerializer
		return ListDocumentSerializer

	def get_queryset(self):
		serializer = self.request.query_params.get('serializer')
		if serializer == "get":
			return Document.objects.select_related('created_by', 'company')
		return Document.objects.all()