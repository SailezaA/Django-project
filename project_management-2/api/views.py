from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Project, ProjectMember, Task, Comment
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, CommentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'], url_path='project/(?P<project_id>[^/.]+)')
    def list_by_project(self, request, project_id=None):
        tasks = Task.objects.filter(project_id=project_id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='project/(?P<project_id>[^/.]+)')
    def create_for_project(self, request, project_id=None):
        data = request.data.copy()
        data['project'] = project_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=['get'], url_path='task/(?P<task_id>[^/.]+)')
    def list_by_task(self, request, task_id=None):
        comments = Comment.objects.filter(task_id=task_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='task/(?P<task_id>[^/.]+)')
    def create_for_task(self, request, task_id=None):
        data = request.data.copy()
        data['task'] = task_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)