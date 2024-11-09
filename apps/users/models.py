from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextChoices, OneToOneField, CASCADE, TextField, IntegerField, ForeignKey, \
    ImageField, BooleanField, TimeField, DateField, DecimalField, DateTimeField


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


class Product(Model):
    name = CharField(max_length=255)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = IntegerField(default=0)
    image = ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True)
    pharmacy = ForeignKey(Pharmacy, on_delete=CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Cart(Model):
    client = ForeignKey(Client, on_delete=CASCADE, related_name='cart')

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.client.user.user.username}"


class CartItem(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name='items')
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = IntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(Model):
    client = ForeignKey(Client, on_delete=CASCADE, related_name='orders')
    total_amount = DecimalField(max_digits=10, decimal_places=2)
    payment_status = BooleanField(default=False)
    order_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.client.user.user.username}"


class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='items')
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = IntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Payment(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='payment')
    payment_method = CharField(max_length=50)  # e.g., 'Visa', 'Mastercard'
    amount = DecimalField(max_digits=10, decimal_places=2)
    success = BooleanField(default=False)
    payment_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {'Success' if self.success else 'Failed'}"
