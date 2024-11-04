from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseTask(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_process', 'In Process'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title} - Status: {self.status}"


class TaskManager(models.Manager):

    def filter_by_status(self, user, status):
        return self.filter(user=user, status=status)


class Task(BaseTask):

    due_date = models.DateField(null=True, blank=True)

    objects = TaskManager()

    def __str__(self):
        return f"{self.title} - Due on {self.due_date}"


class SpecialTaskManager(models.Manager):
    def filter_by_special_day(self, user, date):
        return self.filter(user=user, special_date=date)


class SpecialTask(BaseTask):

    special_date = models.DateField()  

    objects = SpecialTaskManager()  

    def __str__(self):
        return f"{self.title} - Special on {self.special_date}"
