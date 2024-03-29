# Generated by Django 3.1.5 on 2021-05-19 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('hall_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
                ('number_of_rooms', models.IntegerField()),
                ('number_in_room', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('stud_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('fname', models.CharField(max_length=200)),
                ('lname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(max_length=20)),
                ('matric', models.CharField(max_length=20)),
                ('password', models.TextField()),
                ('hall_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.hall')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('fname', models.CharField(max_length=200)),
                ('lname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.TextField()),
                ('hallid', models.IntegerField()),
                ('hall_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.hall')),
            ],
        ),
    ]
