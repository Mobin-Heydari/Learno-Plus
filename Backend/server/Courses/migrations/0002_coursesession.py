# Generated by Django 5.1.2 on 2024-11-09 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='Courses/Sesion/Videos')),
                ('title', models.CharField(max_length=60)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Session', to='Courses.course')),
            ],
            options={
                'verbose_name': 'SesionCourse',
                'verbose_name_plural': 'SesionesCourse',
            },
        ),
    ]
