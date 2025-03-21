from django.db import models
from user.models import CustomUser

# Create your models here.
class Hotel(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    hotel_image = models.ImageField(upload_to='hotels/', default='hotel_default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    class Category(models.TextChoices):
        Starter = 'Starter',
        Main_Course = 'Main Course',
        Dessert = 'Dessert',
        Beverage = 'Beverage',

    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    menu_image = models.ImageField(upload_to='menu')
    price = models.IntegerField()
    category = models.CharField(max_length=50,choices=Category.choices, default=Category.Main_Course)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.title}"


class Order(models.Model):
    class Status(models.TextChoices):
        Packing = 'Packing',
        InTransit = 'In-transit',
        Delivered = 'Delivered',
        Cancelled = 'Cancelled',
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost = models.IntegerField( default=0)
    status = models.CharField(max_length=50, choices=Status.choices, default= Status.Packing)

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price