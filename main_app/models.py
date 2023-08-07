from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# AbstractUser
from django.core import validators

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User, through='TeamMember', related_name='projects')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'project_id': self.id})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super(Project, self).save(*args, **kwargs)
            TeamMember.objects.create(project=self, user=self.created_by)
        else:
            super().save(*args, **kwargs)

class ProjectNote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    note = models.TextField(max_length=150)

    def __str__(self):
        return f"{self.note} is a note for {self.project}"

# Define after project.
# we essentailly want team member to serve as an intermediary between users
# and projects. we needed a second way to access it.
# by using 'through' up above we are effictively able to use users twice
class TeamMember(models.Model):
    #use related_name=to avoid the errors
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_member')
    project= models.ForeignKey(Project, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username
    
class Task(models.Model): 
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    due_date = models.DateField()
    status = models.BooleanField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.name} is a task for {self.project} due on {self.due_date}"

    def save(self, *args, **kwargs):
        if not self.project_id:
            self.project_id = project_id
        super (Task, self).save(*args, **kwargs)

    @property
    def status_display(self):
        return "Complete" if self.status else "Incomplete"

class Photo(models.Model):
    url = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for project_id: {self.project_id} @{self.url}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    bio = models.TextField(max_length=200)
    
    first_name = models.CharField(('first name'), max_length=150, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
    email = models.EmailField(('email address'), blank=True)
    
    def __str__(self):
        return self.user.username

class ProfilePhoto(models.Model):
    url = models.CharField(max_length=200)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    key = models.CharField(max_length=200, default='')

    def __str__(self):
        return f"Photo for user_id: {self.user_profile_id} @{self.url}"

