from django.forms import ModelForm
from django import forms
from .models import Task, Project

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

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

