from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextChoices, OneToOneField, CASCADE, TextField, IntegerField, ForeignKey, \
    ImageField, BooleanField, TimeField, DateField, DecimalField


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
    fee = IntegerField(default=0)

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
    payment_status = BooleanField(default=False)

    @property
    def consultation_fee(self):
        return self.doctor.price

    @property
    def admin_fee(self):
        return self.doctor.hospital.fee

    @property
    def total(self):
        return self.consultation_fee + self.admin_fee

    def __str__(self):
        return f"Booking for {self.client.user.user.username} with {self.doctor.name}"


class Wallet(Model):
    user = OneToOneField(User, CASCADE, related_name='wallet')
    balance = DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"
