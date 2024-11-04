from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Task, SpecialTask
from .serializers import TaskSerializer, SpecialTaskSerializer

# Task API
class TaskAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        filter_param = request.query_params.get('filter')
        tasks = Task.objects.filter(user=request.user)
        
        if filter_param == 'daily':
            tasks = tasks.filter(due_date=timezone.now().date())
        elif filter_param == 'weekly':
            tasks = tasks.filter(due_date__week=timezone.now().isocalendar()[1])
        elif filter_param == 'monthly':
            tasks = tasks.filter(due_date__month=timezone.now().month)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Special Task API
class SpecialTaskAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        special_date = request.query_params.get('special_date')
        tasks = SpecialTask.objects.filter(user=request.user)

        if special_date:
            tasks = tasks.filter(special_date=special_date)

        serializer = SpecialTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = SpecialTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        task = get_object_or_404(SpecialTask, pk=pk, user=request.user)
        serializer = SpecialTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        task = get_object_or_404(SpecialTask, pk=pk, user=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
