from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextChoices, OneToOneField, CASCADE, TextField, IntegerField, ForeignKey


class User(AbstractUser):
    phone_number = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username


class Profile(Model):
    class Type(TextChoices):
        DOCTOR = 'doctor', 'Doctor'
        PHARMACY = 'pharmacy', 'Pharmacy'
        HOSPITAL = 'hospital', 'Hospital'
        CLIENT = 'client', 'Client'

    role = CharField(max_length=10, choices=Type.choices, default=Type.CLIENT)
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Hospital(Model):
    user = OneToOneField(Profile, on_delete=CASCADE)
    about = TextField()
    location = TextField()


class Doctor(Model):
    user = OneToOneField(Profile, on_delete=CASCADE)
    about = TextField()
    price = IntegerField(default=0)
    hospital = ForeignKey(Hospital, on_delete=CASCADE)


class Pharmacy(Model):
    user = OneToOneField(Profile, on_delete=CASCADE)
    about = TextField()
    location = TextField()


class Client(Model):
    user = OneToOneField(Profile, on_delete=CASCADE)
    name = CharField(max_length=255)
    weight = IntegerField()
    height = IntegerField()
    blood_pressure = IntegerField()
