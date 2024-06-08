from django.http import Http404
from .serializers import *
from rest_framework import viewsets, permissions, status
from .models import Company, Document
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, Case, When
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action, api_view, permission_classes
import re
from rest_framework.filters import SearchFilter
import django_filters.rest_framework


class CompanyView(viewsets.ModelViewSet):
    filter_fields = "industry"

    def perform_create(self, serializer):
        serializer.save(created_by_id=self.request.user.id)

    def get_serializer_class(self):
        serializer = self.request.query_params.get("serializer")
        if serializer == "create":
            return CreateCompanySerializer
        elif serializer == "get":
            return GetCompanySerializer
        return ListCompanySerializer

    def get_queryset(self):
        serializer = self.request.query_params.get("serializer")
        owner = self.request.query_params.get("owner")
        companies = Company.objects

        if owner:
            try:
                companies.get(created_by__username=owner)
            except Company.DoesNotExist:
                raise Http404

        if serializer == "get":
            return companies.select_related("created_by").prefetch_related("managed_by")
        return companies.all()

    def get_permissions(self):
        serializer = self.request.query_params.get("serializer")
        if self.request.method == "GET" and serializer == "get":
            return [permissions.AllowAny()]
        return super().get_permissions()


class UserView(viewsets.ModelViewSet):
    search_fields = ("username",)
    filterset_fields = {"username": ["exact", "in"], "id": ["exact", "in"]}

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetUserSerializer
        return UserSerializer

    def get_queryset(self):
        return User.objects.all()

    @action(detail=True, methods=["post"], url_path="change-password")
    def change_password(self, request, pk=None):
        password_pattern = (
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-_]).{8,}$"
        )
        with transaction.atomic():
            user = self.get_object()
            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            if not user.check_password(old_password):
                raise ValidationError("Old password is wrong.")

            if confirm_password != new_password:
                raise ValidationError("Password fields are not matched.")

            if not re.match(password_pattern, new_password):
                raise ValidationError(
                    "Password must contain minimum 8 characters,\n uppercase letter, lowercase letter, digit and a special character."
                )

            user.set_password(new_password)
            user.save()

            return Response("Password updated successfully", status=status.HTTP_200_OK)


class DocumentView(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(created_by_id=self.request.user.id)

    def get_serializer_class(self):
        serializer = self.request.query_params.get("serializer")
        if serializer == "create":
            return CreateDocumentSerializer
        elif serializer == "get":
            return GetDocumentSerializer
        return ListDocumentSerializer

    def get_queryset(self):
        serializer = self.request.query_params.get("serializer")
        if serializer == "get":
            return Document.objects.select_related("created_by", "company")
        return Document.objects.all()


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def register(request):
    data = request.data
    username = data.get("username")
    first_name = data.get("first_name") or ""
    last_name = data.get("last_name") or ""
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    mobile = data.get("mobile")
    address = data.get("address")
    national_id = data.get("national_id")

    # Required Fields
    for field in ["username", "email", "password", "confirm_password"]:
        if not data.get(field):
            raise ValidationError(f"{field.replace('_',' ').capitalize()} is required.")

    # Unique Fields
    users = User.objects.filter(
        Q(username=username)
        | Q(email=email)
        | Q(profile__mobile=mobile)
        | Q(profile__national_id=national_id)
    ).values("username", "email", "profile__mobile", "profile__national_id")

    for user in users:
        if user.get("username") == username:
            raise ValidationError(
                "This username is already used, please try another one."
            )

        if user.get("email") == email:
            raise ValidationError(
                "This email already exists, if this is your account and you can not login please use forget password"
            )

        if mobile and user.get("profile__mobile") == mobile:
            raise ValidationError("This mobile number already used before.")
        if national_id and user.get("profile__national_id") == national_id:
            raise ValidationError("This national id already exists.")

    password_pattern = (
        r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-_]).{8,}$"
    )

    # Validations
    if confirm_password != password:
        raise ValidationError("Password fields are not matched.")

    if not re.match(password_pattern, password):
        raise ValidationError(
            "Password must contain minimum 8 characters,\n uppercase letter, lowercase letter, digit and a special character."
        )
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(email_pattern, email):
        raise ValidationError("Invalid Email.")

    national_id_pattern = r"(2|3)[0-9]{13}$"
    if national_id and not re.match(national_id_pattern, national_id):
        raise ValidationError("Invalid National ID.")

    mobile_pattern = r"(01)[0-9]{9}$"
    if mobile and not re.match(mobile_pattern, mobile):
        raise ValidationError("Invalid Modile Number.")

    user = User.objects.create(
        first_name=first_name, last_name=last_name, username=username, email=email
    )
    user.set_password(password)
    user.save()
    user.profile.national_id = national_id
    user.profile.mobile = mobile
    user.profile.address = address
    user.profile.save()

    return Response("Successfully created", status=status.HTTP_201_CREATED)
