from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_receptionist = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)



class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE,related_name='rec')

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doc')
    specialty = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Record(models.Model):
    patient = models.ForeignKey(Patient, on_delete= models.CASCADE, related_name='records')
    created_by = models.ForeignKey(Doctor, on_delete= models.DO_NOTHING, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=4000)

    def __str__(self):
        return self.text


class Appointment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')

    def __str__(self):
        return self.time


