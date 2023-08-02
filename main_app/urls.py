from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/user_login/', views.user_login, name='user_login'),    
    path('projects/', views.projects_index, name='index'),
    path('projects/create/', views.ProjectCreate.as_view(), name='projects_create'),
    path('projects/<int:project_id>/', views.projects_detail, name='detail'),
    path('projects/<int:pk>/update/', views.ProjectUpdate.as_view(), name='projects_update'),
    path('projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name='projects_delete'),
    path('projects/<int:project_id>/add_task/', views.add_task, name='add_task'),
    path('projects/<int:project_id>/assoc_member/<int:team_member_id>/',views.assoc_member, name='assoc_member'),
    path('projects/<int:project_id>/unassoc_member/<int:team_member_id>/',views.unassoc_member, name='unassoc_member'),
    path('projects/<int:project_id>/add_photo/',views.add_photo, name='add_photo'),
]