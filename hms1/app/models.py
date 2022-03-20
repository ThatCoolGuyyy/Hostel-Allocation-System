from django.db import models

# Create your models here.


class Hall(models.Model):
    hall_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    number_of_rooms = models.IntegerField()
    number_in_room = models.CharField(max_length=20)
    def __str__(self):
        return (self.name +" " + str(self.hall_id))


class Student(models.Model):
    stud_id = models.IntegerField(primary_key=True, unique=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    matric = models.CharField(max_length=20, default="")
    room_number = models.CharField(max_length=20)
    hallid = models.IntegerField(default=0)
    pending = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    password = models.TextField()
    def __str__(self):
        return (self.fname + " " + self.lname + " " + self.matric)
        

class Admin(models.Model):
    admin_id = models.IntegerField(primary_key=True, unique=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.TextField()
    hallid = models.IntegerField()
    def __str__(self):
        return self.fname

class Messages(models.Model):
    hallid = models.IntegerField(default=1, primary_key=True)
    sender_id = models.IntegerField()
    sender_name = models.CharField(max_length=200)
    message = models.TextField(max_length=200)
    date = models.CharField(max_length=20)

    def __str__(self):
        return self.message