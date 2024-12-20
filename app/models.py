from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images') #pip install pillow
    desc=models.TextField()
    mark_price=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    descount_percent = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    price=models.DecimalField(default=0.00,max_digits=10,decimal_places=2,editable=False)
    date=models.DateField(auto_now=True)
    About_course=models.TextField(blank=True)


    def save(self,*args, **kwargs):
        self.price=self.mark_price *(1-self.descount_percent/100)
        super().save(*args, **kwargs)

    
    def __str__(self) -> str:
        return self.name

    
class Student(models.Model):
    name=models.CharField(max_length=50)
    contact=models.CharField(max_length=13)
    email=models.EmailField()
    message=models.TextField()
    age=models.IntegerField(default=0)
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to="images",blank=True,null=True)
    address=models.CharField(max_length=20)
    phone=models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.course.name



class Cart(models.Model):
    cart_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_id.username

class CartItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='item_list')
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    @property
    def total_price(self):
        return self.course.price * self.quantity

    def __str__(self):
        return self.course.name


 


class Order(models.Model):
    name = models.CharField(blank=True, max_length=50)
    order_id = models.CharField(max_length=6, null=True, unique=True)
    phone_number = models.CharField(default=0,max_length=20)
    Address = models.TextField(blank=True)
    total_price = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name



class Certificate(models.Model):
    certificate_number = models.CharField(max_length=255, unique=True)
    issued_to = models.CharField(max_length=255)

    