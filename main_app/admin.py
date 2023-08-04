from django.contrib import admin
from .models import Project, Task, TeamMember, Photo, UserProfile, ProfilePhoto

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TeamMember)
admin.site.register(Photo)
admin.site.register(UserProfile)
admin.site.register(ProfilePhoto)
