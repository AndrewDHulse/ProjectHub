# Generated by Django 4.2.3 on 2023-08-06 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_remove_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.userprofile'),
        ),
    ]
