from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, ImageField, IntegerField


# Create your models here.
class Category(Model):
    name = CharField(max_length=255)


class DoctorDetail(Model):
    name = CharField(max_length=255)
    type = ForeignKey(Category, CASCADE)
    description = TextField()
    image = ImageField(upload_to='doctors/%Y/%m/%d/')
    score = IntegerField(default=0)
