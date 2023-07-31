from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('projects/', views.projects_index, name='index'),
    path('projects/create/', views.ProjectCreate.as_view(), name='projects_create'),
    path('projects/<int:project_id>/', views.projects_detail, name='detail'),

]