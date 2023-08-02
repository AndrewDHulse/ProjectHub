from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# AbstractUser

# Create your models here.




# class CustomUser(AbstractUser):
#     #fix profile_picture later
#     profile_picture= models.ImageField()
    

#     def __str__(self):
#         return self.user_name



class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField() 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # use related_name= to avoid the conflict error's we've been given
    # use through model, see bellow
    team_members = models.ManyToManyField(User, through='TeamMember', related_name='projects')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'project_id': self.id})


#we did it!


#Define after project.
#we essentailly want team member to serve as an intermediary between users
# and projects. we needed a second way to access it.
# by using through up above we are effictively able to use users twice
class TeamMember(models.Model):
    #use related_name=to avoid the errors we've been given
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

    def __str__(self):
        return f"{self.name} is a task for {self.project} due on {self.due_date}"
    

class Photo(models.Model):
    url = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for project_id: {self.project_id} @{self.url}"
    
