# Generated by Django 3.1.5 on 2021-05-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_student_pending'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hallid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='pending',
            field=models.BooleanField(default=True),
        ),
    ]
