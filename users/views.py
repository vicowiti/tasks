# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import User
# from .serializers import UserSerializer
# from .permissions import IsAdmin

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by("id")
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated & IsAdmin]
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsAdmin]


@extend_schema(
    tags=["Users"],
    description="Change default password and set has_default_password to false.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "old_password": {"type": "string"},
                "new_password": {"type": "string"}
            },
            "required": ["old_password", "new_password"]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            }
        },
        400: {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            }
        }
    }
)
class ChangeDefaultPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old = request.data.get("old_password")
        new = request.data.get("new_password")

        if not old or not new:
            return Response({"detail": "old_password and new_password are required"}, status=400)

        if not check_password(old, user.password):
            return Response({"detail": "Old password is incorrect"}, status=400)

        user.set_password(new)
        user.has_default_password = False
        user.save()

        return Response({"detail": "Password changed successfully"}, status=200)
