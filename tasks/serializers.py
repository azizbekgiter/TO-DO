from rest_framework import serializers
from .models import Task, SpecialTask

class BaseTaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'user', 'title', 'description', 'status', 'created_at', 'updated_at']
        

class TaskSerializer(BaseTaskSerializer):
    user = serializers.StringRelatedField()  

    class Meta(BaseTaskSerializer.Meta):
        model = Task
        fields = BaseTaskSerializer.Meta.fields + ['due_date']
        read_only_fields = ['user']

class SpecialTaskSerializer(BaseTaskSerializer):
    user = serializers.StringRelatedField() 

    class Meta(BaseTaskSerializer.Meta):
        model = SpecialTask
        fields = BaseTaskSerializer.Meta.fields + ['special_date']
        read_only_fields = ['user']
