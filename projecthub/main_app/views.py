from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Project
# Create your views here.

def home(request):
  return render(request, 'home.html')

@login_required
def projects_index(request):
  projects = Project.objects.filter(user=request.user)
  return render(request, 'projects/index.html', {
    'projects': projects
  })

class ProjectCreate(LoginRequiredMixin, CreateView):
  model = Project
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)



def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
        error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {'form' : form, 'error_message' : error_message}
  return render (request, 'registration/signup.html', context)

@login_required
def projects_detail(request, project_id):
  project = Project.objects.get(id=project_id)

  return render(request, 'projects/detail.html', {
    'project': project
  })

