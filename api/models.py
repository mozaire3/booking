from django.db import models
from bson import ObjectId
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserModel(AbstractUser):
    full_name = models.CharField(max_length=40)
    email = models.CharField(max_length=255,unique=True)
    # password = models.CharField(max_length=255)
    role = models.IntegerField()
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='static/public/profile',default=None, blank=True, null=True)   
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
# def upload_path(instance,filename):
#     return '/'.join(['covers',str(instance.course_name),filename])
    
class HotelModel (models.Model):
    titre = models.CharField(max_length=100,default=None, blank=True, null=True)
    country = models.CharField(max_length=100,default=None, blank=True, null=True)
    town = models.CharField(max_length=100,default=None, blank=True, null=True)
    titre_fon =  models.CharField(max_length=100,default=None, blank=True, null=True)
    description = models.CharField(max_length=500,default=None, blank=True, null=True)
    description_fon = models.CharField(max_length=500,default=None, blank=True, null=True)
    audio = models.CharField(max_length=1000,default=None, blank=True, null=True)
    imageCourse = models.FileField(upload_to='static/public',default=None, blank=True, null=True)
    price = models.DecimalField(max_digits=10000000000, decimal_places= 2,default=None, blank=True, null=True)


class PayementModel(models.Model):
    payementDate = models.DateField(auto_created=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payementMethod = models.CharField(max_length=50)



class RoomsModel(models.Model):
    hotelID = models.CharField(max_length=1000,default=None)
    title = models.CharField(max_length=1000,default=None)
    size =  models.CharField(max_length=1000,default=None, blank=True, null=True)
    title_fon = models.CharField(max_length=1000,default=None)
    image = models.FileField(upload_to='static/public/image',default=None, blank=True, null=True)
    audio = models.CharField(max_length=1000,default=None, blank=True, null=True)
    content = models.CharField(max_length=1000,default=None, blank=True, null=True)
    content_fon = models.CharField(max_length=1000,default=None, blank=True, null=True)
    price = models.DecimalField(max_digits=10000000000, decimal_places= 1,default=None, blank=True, null=True)

    
    
    
    


