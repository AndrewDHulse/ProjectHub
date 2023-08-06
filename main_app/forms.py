from django.forms import ModelForm
from django import forms
from .models import Task, Project, UserProfile, ProjectNote

class TaskForm(ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%m-%d-%Y', '%m/%d/%Y', '%Y-%m-%d'],
        required=False       
    )
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'status', 'assigned_to']
        widgets = {'project': forms.HiddenInput()} 

class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%m-%d-%Y', '%m/%d/%Y', '%Y-%m-%d'],
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%m-%d-%Y', '%m/%d/%Y', '%Y-%m-%d'],
        required=False       
    )
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'bio', 'email']

class ProjectNoteForm(forms.ModelForm):
    class Meta:
        model = ProjectNote
        fields = ['note']

