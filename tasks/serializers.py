from rest_framework import serializers
from .models import Task
from users.serializers import UserSerializer
from users.models import User

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    created_by = serializers.ReadOnlyField(source="created_by.id")
    created_by_username = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "deadline", "assignee", "created_by", "created_at", "updated_at", "created_by_username")
        read_only_fields = ("id", "created_at", "updated_at", "created_by")