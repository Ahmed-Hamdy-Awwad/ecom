from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile = models.CharField(max_length=100, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	national_id = models.CharField(max_length=100, null=True, blank=True)


class Company(models.Model):
	INDUSTRY_CHOICES=(
		("TR", "Trading",),
		("PC", "Petrochemics",)
	)
	name = models.CharField(max_length=100)	
	email = models.CharField(max_length=100)
	mobile = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	tax_number = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES)
	managed_by = models.ManyToManyField(User, related_name='managed_companies')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_companies')

	def __str__(self):
		return self.name


class Document(models.Model):
	issue_date = models.DateField()
	name = models.CharField(max_length=100)
	approved = models.BooleanField(default=False)
	file = models.FileField(upload_to='documents/')
	created_at = models.DateTimeField(auto_now_add=True)
	expiry_date = models.DateField(null=True, blank=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_documents')

	def __str__(self):
		return self.name