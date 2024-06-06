from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from .process import process


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def ocr_process(request):
    file = request.FILES["file"]
    data = process(file)
    return Response(data, status=status.HTTP_201_CREATED)
