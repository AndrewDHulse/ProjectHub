import uuid
import boto3
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm, ProjectForm, UserProfileForm, ProjectNoteForm, ProjectUpdateForm
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Project, TeamMember, Photo, Task, UserProfile, ProfilePhoto, ProjectNote
from django.utils.dateparse import parse_date

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

@login_required
def projects_update(request, project_id):
    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('detail', project_id=project_id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/update_project.html', {'form': form})
    
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
    if request.method == 'POST':
      project_update_form = ProjectUpdateForm(request.POST, instance=project)
      if project_update_form.is_valid():
        project_update_form.save()
        return redirect('detail', project_id=project_id)

    else:
        project_update_form = ProjectForm(instance=project)
    #grabbed users here
    all_users = User.objects.all()
    # check team members here
    team_members_id = project.team_members.all()
    # filter team members from all users
    members_not_in_team = all_users.exclude(id__in=team_members_id)
    task_form = TaskForm()
    project_note_form = ProjectNoteForm()
    tasks= Task.objects.filter(project_id=project_id)
    project_notes = ProjectNote.objects.filter(project_id=project_id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'task_form': task_form,
        'project_note_form' : project_note_form,
        'members_not_in_team': members_not_in_team,
        'tasks' : tasks,
        'project_notes' : project_notes,
        'project_update_form' : project_update_form
    })

@login_required
def add_task(request, project_id):
  project= Project.objects.get(pk=project_id)
  if request.method == 'POST':
    form = TaskForm(request.POST)
    if form.is_valid():
      new_task = form.save(commit=False)
      new_task.project_id = project_id
      new_task.project=project
      new_task.save()
    return redirect('detail', project_id=project_id)
  else:
    form = TaskForm()
  tasks = Task.objects.filter(project=project)

  context = {
    'project' : project,
    'tasks' : tasks,
    'task_form' : form,
  }
  return render(request, 'detail.html', context)

@login_required
def update_task(request, task_id):
  if request.method == 'POST':
    task = Task.objects.get(pk=task_id)
    new_status = request.POST.get('status', False) == 'on' 
    task.status = new_status
    task.save()

  return redirect('detail', project_id=task.project_id)

@login_required
def add_project_note(request, project_id):
  form = ProjectNoteForm(request.POST)
  print(f"before form is valid: {form}")
  if form.is_valid():
    new_note = form.save(commit=False)
    new_note.project_id = project_id
    new_note.save()
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


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'user_profile.html'

    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=user_profile)
        print(f" get for user_profile,(id): {user_profile}, ({user_profile.id}), req.user.id: {request.user.id}")
        return render(request, self.template_name, {'form': form, 'user_profile': user_profile})

    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            print(f"form post is valid for user_profile: {user_profile}")
            form.save()
            print(f"form post SAVED for user_profile: {user_profile}")
            return redirect('user_profile')
        return render(request, self.template_name, {'form': form, 'user_profile': user_profile})


@login_required
def add_user_photo(request, user_profile_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    print(f"I have reached the add_user_photo URL")
    if photo_file:
        s3 = boto3.client('s3')        
        key = uuid.uuid4().hex[:6] + photo_file.name[:photo_file.name.rfind('.')]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign profilephoto to req.user.userprofile
            # since that's the object w One:One relationship           
            profilephoto = request.user.userprofile.profilephoto
            if profilephoto:
              if profilephoto.key:
                s3.delete_object(Bucket=bucket, Key=profilephoto.key)
                print(f"the old user_profilephoto was deleted") 
              # Now update the key, url for profilephoto and save to db             
              profilephoto.key = key
              profilephoto.url = url
              profilephoto.save()
            else:
              ProfilePhoto.objects.create(url=url, user_profile_id=user_profile_id, key=key)
              print('We made it to try part')
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('user_profile')

