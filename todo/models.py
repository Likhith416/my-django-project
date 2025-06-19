from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # 👥 User model

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)  # 📅 Due date
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 👥 User ownership

    def __str__(self):
        return self.title
