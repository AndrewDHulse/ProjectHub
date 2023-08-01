from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

    

class Project(models.Model):
    name = models.CharField(max_length=50)
    # Insert more attributes here:
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'project_id': self.id})

class Task(models.Model): 
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    due_date = models.DateField()
    status = models.BooleanField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} is a task for {self.project} due on {self.due_date}"
    

    