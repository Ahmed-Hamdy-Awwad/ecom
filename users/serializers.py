from .models import Company
from rest_framework import serializers
from django.contrib.auth.models import User


class CreateCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		exclude = ['created_by', 'managed_by']


class GetCompanySerializer(serializers.ModelSerializer):
	created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
	managed_by = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)
	class Meta:
		model = Company
		fields = "__all__"


class ListCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = "__all__"