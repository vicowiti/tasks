from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from users.models import User
from users.permissions import IsAssigneeOrReadOnly
from django.db.models import Count



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsAssigneeOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend ]
    search_fields = ["title", "description"]
    ordering_fields = ["deadline", "created_at", "status"]
    filterset_fields = ["status"]

    # Role-based queryset
    def get_queryset(self):
        user = self.request.user

        if user.is_admin() or user.is_manager():
            return Task.objects.all().select_related("assignee", "created_by")

        return Task.objects.filter(
            assignee=user
        ).select_related("assignee", "created_by")

    # Create
    def perform_create(self, serializer):
        creator = self.request.user
        assignee = serializer.validated_data.get("assignee", None)

        if not (creator.is_manager() or creator.is_admin()):
            serializer.save(created_by=creator, assignee=creator)
        else:
            serializer.save(created_by=creator)

    # Custom Action: Get tasks by any user (Admin/Manager only)
    @action(detail=False, methods=["GET"], url_path="by-user/(?P<user_id>[^/.]+)")
    def get_tasks_by_user(self, request, user_id=None):
        user = request.user

        if not (user.is_admin() or user.is_manager()):
            return Response({"detail": "Not authorized"}, status=403)

        target_user = get_object_or_404(User, id=user_id)

        tasks = Task.objects.filter(
            assignee=target_user
        ).select_related("assignee", "created_by")

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], url_path="init")
    def init_dashboard(self, request):
        user = request.user

        # Role-based queryset
        if user.is_admin() or user.is_manager():
            qs = Task.objects.all()
        else:
            qs = Task.objects.filter(assignee=user)

        # Stats
        stats = {
            "total_tasks": qs.count(),
            "todo_tasks": qs.filter(status="TODO").count(),
            "in_progress_tasks": qs.filter(status="IN_PROGRESS").count(),
            "done_tasks": qs.filter(status="DONE").count(),
        }

        # Summary tasks - latest 5
        summary_tasks = qs.order_by("-created_at")[:5]
        serializer = self.get_serializer(summary_tasks, many=True)

        return Response({
            "stats": stats,
            "summary_tasks": serializer.data
        })

