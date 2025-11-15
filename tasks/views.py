# tasks/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from users.permissions import IsAssigneeOrReadOnly, IsManagerOrAdmin

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related("assignee", "created_by")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsAssigneeOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["deadline", "created_at", "status"]

    def perform_create(self, serializer):
        # allow managers/admins to assign; else assign to creator or null
        creator = self.request.user
        assignee = serializer.validated_data.get("assignee", None)
        # Non-manager users cannot assign tasks to others; ensure only manager/admin can set assignee
        if not (creator.is_manager() or creator.is_admin()):
            # force assignee to creator
            serializer.save(created_by=creator, assignee=creator)
        else:
            serializer.save(created_by=creator)
