from django.db import models

# Create your models here.

role = (
    ("Tourist","Tourist"),
    ("Agent","Agent"),
)

class User(models.Model):
    role = models.CharField(choices= role, max_length=30)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    contact = models.PositiveIntegerField()
    address = models.TextField()
    age = models.BigIntegerField(null=True)    
    password = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='user_profile/',default="userprofile.png")
    disignation = models.CharField(max_length=50 , null=True)
    facebooklink = models.URLField(max_length=200,null=True)
    instagram = models.URLField(max_length=200,null=True)
    twiter = models.URLField(max_length=200,null=True)
    
    def __str__(self):
        return self.role + " " + self.name

class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    packagename = models.CharField(max_length=100)
    placename = models.CharField(max_length=100)
    movefrom = models.CharField(max_length=100)
    tofrom = models.CharField(max_length=100)
    movedate = models.DateField()
    todate = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    totaltourist = models.IntegerField()
    Available_slot = models.PositiveIntegerField()
    image = models.ImageField(upload_to='package_images/')

    def __str__(self):
        return self.packagename

class DayDescription(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.package.packagename
    
class PackageImage(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='package_images/')

    def __str__(self):
        return self.package.packagename
    
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    package = models.ForeignKey(Package , on_delete=models.CASCADE)
    packagename = models.CharField(max_length=50)
    packageprice = models.PositiveIntegerField()
    username = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    contact = models.PositiveBigIntegerField()
    address = models.TextField()
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.packagename + " || " + self.username
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()
    
    def __str__(self):
        return self.name + " || " + self.subject