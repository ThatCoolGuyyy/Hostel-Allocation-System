# Generated by Django 3.1.5 on 2021-05-27 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_student_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='room_number',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='matric',
            field=models.CharField(default='', max_length=20),
        ),
    ]
