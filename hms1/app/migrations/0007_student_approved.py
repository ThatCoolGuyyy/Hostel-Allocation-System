# Generated by Django 3.1.5 on 2021-05-21 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210521_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
