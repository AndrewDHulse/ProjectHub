# ProjectHub

ProjectHub is a site built in a collaborative effort between Andrew Hulse and Alex Villalobos. The game is project management. It is first and foremost a productivity tool with teams in mind. Users aree able to easily:
- Create a project 
- Add and remove team members
- Create and update tasks
- Upload photos related to the tasks

<img alt="Screenshot of project detail page" src=/home/andrew/code/projecthub/main_app/static/images/detail-screenshot.png>

## Getting Started

Visit us <a href=https://projecthub-avah-f1fe7fefab0a.herokuapp.com>here</a>   

To begin, the user may click the sign-up button found in the top bar. They will then be directed to create a project. From there, they will find all features to be intuitive, all tools are labeled prominently in the sidebar of the project detail page, and site navigation is made easy by the task bar heading the page.
 
## Features 

- User profile page, to be updated and expanded at a later date
- Index of projects both created by the user, and projects of which they are a member
- Ability to create and delete projects
- Ability to add notes
- Ability to update tasks

## Technologies Used

<div style="display: flex; justify-content: center;">
<!--bootstrap-->
<img alt="Bootstrap Badge" src="https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white">

The implimentation of Bootstrap allows for a cleaner look to project pages. As an example, the task form would otherwise take up too much whitespace for a clean look, but by relagating it to be displayed as a single button:
```
          <button type="button" class="btn btn-primary mb-2" data-bs-toggle="modal"
          data-bs-target="#addTaskModal">
            Add Task
          </button>
```
The much larger form could be called upon only when necessary, without the need to render an entirely new web page
```
<div class="modal fade" id="addTaskModal" tabindex="-1" aria-labelledby="addTaskModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="AddTaskModalLabel">Add Task</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div id="taskForm">
              <form action="{% url 'add_task' project.id %}" method="POST">
                {% csrf_token %}
                <p>Name: </p> {{task_form.name}}
                <br>
                <p> Description: </p> {{task_form.description}}
                <br>
                <p> Due Date: </p> {{task_form.due_date}}
                <br>
                <p> Assigned To: </p> {{task_form.assigned_to}}
              </div>
            </div>
            <div class="modal-footer">
              <input type="submit" class="btn btn-primary" value="submit">
            </form>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
```

<!--Python-->
<img alt="Python Badge" src= "https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
Python's simplicity should not drive one to think it is not a powerful language. This example from ProjectHub's views.py illustrates the language's capability:

```
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
    project_note_form = ProjectNoteForm()
    tasks= Task.objects.filter(project_id=project_id)
    project_notes = ProjectNote.objects.filter(project_id=project_id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'task_form': task_form,
        'project_note_form' : project_note_form,
        'members_not_in_team': members_not_in_team,
        'tasks' : tasks,
        'project_notes' : project_notes
    })
```
In one short codeblock, Python 
- Ensure's proper authorization to view the details page.
- Leverages Django's querysets and forms.
- Properly filter's users for proper team management.



<!--Django-->
<img alt="Django Badge" src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">

Django allows for easy and simple management of the several(7) models within this project.

```
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
            super(Project, self).save(*args, **kwargs)
```
This illustrates the simplicity of overriding the default functionality of django's default behaviors, the ease in creating differing relationships, be it many to many, or many to one. Additionally, the use of a through model of demonstrates an even more powerful method in which django can handle relationships and data queries 

```
class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_member')
    project= models.ForeignKey(Project, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username
```

<!--JavaScript-->
<img alt="Javascript Badge" src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E">

Minimal Javascript was used within HTML to allow for a more user friendly experience. 

```
<script>
  function updateTask(taskId) {
    const formElement = document.getElementById(`form-${taskId}`);
    formElement.submit();
  }
  </script>
```
This function allows users to update tasks from the project details page simply by selecting a checkbox.

<!--HTML5-->
<img alt="HTML5 Badge" src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">

<!-- PostgreSQL -->
<img alt="PostgreSQL badge" src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"> 




<!--CSS-->
<img alt="CSS Badge" src= "https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white">





</div>

## Icebox Features

- Expanded Profiles
- Different roles and permissions between team members and project managers
- Multiple forms, such as spreadsheets and graphs created in-site for projects
- Multiple filetypes allowed for upload
- Ability to sort the index
- Ability to make projects public or private