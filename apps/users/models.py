from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextChoices, OneToOneField, CASCADE, TextField, IntegerField, ForeignKey, \
    ImageField, BooleanField, TimeField, DateField


class User(AbstractUser):
    phone_number = CharField(max_length=255, unique=True, null=True, blank=True)

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
    name = CharField(max_length=255)
    about = TextField()
    location = TextField()
    fee = IntegerField(default=0)  # Add fee field for admin fee

    def __str__(self):
        return f"Hospital {self.user}"


class Doctor(Model):
    user = OneToOneField(Profile, on_delete=CASCADE)
    hospital = ForeignKey(Hospital, on_delete=CASCADE, null=True, blank=True)
    name = CharField(max_length=255)
    description = TextField(null=True, blank=True)
    image = ImageField(upload_to='doctors/%Y/%m/%d/', null=True, blank=True)
    score = IntegerField(default=0)
    price = IntegerField(default=0)

    def __str__(self):
        return f"Doctor {self.user}"


class Pharmacy(Model):
    user = OneToOneField(Profile, on_delete=CASCADE)
    name = CharField(max_length=255)
    about = TextField()
    location = TextField()

    def __str__(self):
        return f"Pharmacy {self.user}"


class Client(Model):
    user = OneToOneField(Profile, on_delete=CASCADE)
    name = CharField(max_length=255)
    weight = IntegerField(null=True, blank=True)
    height = IntegerField(null=True, blank=True)
    blood_pressure = IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Client {self.user}"


class Booking(Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    client = ForeignKey(Client, CASCADE, related_name='bookings')
    doctor = ForeignKey(Doctor, CASCADE, related_name='bookings')
    date = DateField(auto_now_add=True, null=True)
    time = TimeField(auto_now_add=True, null=True)
    reason = CharField(max_length=255)
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    consultation_price = IntegerField()
    admin_fee = IntegerField(default=0)  # New field for admin fee
    payment_status = BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.consultation_price and self.doctor:
            self.consultation_price = self.doctor.price

        if self.doctor and self.doctor.hospital:
            self.admin_fee = self.doctor.hospital.fee

        super().save(*args, **kwargs)

    @property
    def total(self):
        return self.consultation_price + self.admin_fee

    def __str__(self):
        return f"Booking for {self.client.user.user.username} with {self.doctor.name}"
