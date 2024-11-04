from django.urls import path
from .views import TaskAPIView, SpecialTaskAPIView

urlpatterns = [

    path('tasks/', TaskAPIView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', TaskAPIView.as_view(), name='task_update_delete'),
    path('special-tasks/', SpecialTaskAPIView.as_view(), name='special_task_list_create'),
    path('special-tasks/<int:pk>/', SpecialTaskAPIView.as_view(), name='special_task_update_delete'),
]
