from .models import Company
from rest_framework import serializers


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