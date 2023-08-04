import uuid
import boto3
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm, ProjectForm, UserProfileForm
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Project, TeamMember, Photo, Task, UserProfile

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def projects_index(request):
  projects = Project.objects.filter(team_members=request.user)
  return render(request, 'projects/index.html', {
    'projects': projects
  })

# class ProjectCreate(LoginRequiredMixin, CreateView):
#   model = Project
#   fields = ['name', 'description', 'start_date', 'end_date']

#   def form_valid(self, form):
#     form.instance.created_by = self.request.user
#     return super().form_valid(form)

class ProjectCreate(LoginRequiredMixin, CreateView):
  model = Project
  form_class = ProjectForm
  template_name = 'main_app/project_form.html'

  def form_valid(self, form):
    form.instance.created_by = self.request.user
    return super().form_valid(form)

class ProjectDelete(LoginRequiredMixin, DeleteView):
  model = Project
  success_url = '/projects'

class ProjectUpdate(LoginRequiredMixin, UpdateView):
  model = Project
  fields = '__all__'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
        error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {'form' : form, 'error_message' : error_message}
  return render (request, 'registration/signup.html', context)

@login_required
def projects_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    #grabbed users here
    all_users = User.objects.all()
    # check team members here
    team_members_id = project.team_members.all()
    # filter team members from all users
    members_not_in_team = all_users.exclude(id__in=team_members_id)
    task_form = TaskForm()
    tasks= Task.objects.filter(project_id=project_id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'task_form': task_form,
        'members_not_in_team': members_not_in_team,
        'tasks' : tasks,
    })

@login_required
def add_task(request, project_id):
  form = TaskForm(request.POST)
  if form.is_valid():
    new_task = form.save(commit=False)
    new_task.project_id = project_id
    new_task.save()
  return redirect('detail', project_id=project_id)

@login_required
def assoc_member(request, project_id, team_member_id):
  Project.objects.get(id=project_id).team_members.add(team_member_id)
  return redirect('detail', project_id=project_id)

@login_required
def unassoc_member(request, project_id, team_member_id):
  Project.objects.get(id=project_id).team_members.remove(team_member_id)
  return redirect('detail', project_id=project_id)

@login_required
def add_photo(request, project_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        # It needs to keep the same file extension of
        # the file that was uploaded (.png, .jpeg, etc..)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, project_id=project_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', project_id=project_id)

def user_login(request):
    error_message = ''
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
            else:
                error_message = 'Invalid login - try again'
    else:
        form = AuthenticationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'user_login.html', context)

# @login_required
# def user_profile(request, user_id):
#     error_message = ''    
#     user_profile = UserProfile.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#           form.save()
#           return redirect('user_profile')
#     else:
#         error_message = 'Ugh Oh, something went wrong!'
    
#     form = UserProfileForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'user_profile.html', context, {
#        'user_profile': user_profile,       
#     })

@login_required
def user_profile(request):
    error_message = ''
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            error_message = 'Ugh Oh, something went wrong!'
    else:
        form = UserProfileForm()
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'user_profile.html', context)
