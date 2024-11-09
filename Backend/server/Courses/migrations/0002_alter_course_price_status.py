# Generated by Django 5.1.2 on 2024-11-09 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price_status',
            field=models.CharField(choices=[('FREE', 'Free'), ('PAID', 'Paid')], default='FREE', max_length=5),
        ),
    ]
