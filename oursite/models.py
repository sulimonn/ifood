from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class User(AbstractUser):
    phone_number = models.IntegerField(blank=True, null=True)
    current_address = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)

    
class Filter(models.Model):

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Restaurant(models.Model):

    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, db_index=True, verbose_name="Url")
    cat = models.ForeignKey(Filter,  on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='oursite/images/restImages/', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("restaurant", kwargs={"rest_slug": self.slug})


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    amount = models.IntegerField()
    orderDate = models.DateTimeField(auto_now_add=True)
    delivery = models.IntegerField()
    service = models.IntegerField()

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.pk)


class RestLocation(models.Model):

    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    loc = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rest)


class FoodFilter(models.Model):
    title = models.CharField(max_length=50)
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['rest', 'title']


class Menu(models.Model):
    title = models.CharField(max_length=50)
    cat = models.ForeignKey(FoodFilter, on_delete=models.CASCADE, null=True)
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    photo = models.ImageField(upload_to='oursite/images/menuImages/', null=True)
    
    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menu"

    def __str__(self):
        return self.title


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.pk)


class UserCart(models.Model):
    food = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField(null=True)
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.rest = self.food.rest
        if self.quantity is None:
            self.quantity = 1
        self.total = self.quantity * self.food.price
        super(UserCart, self).save(*args, **kwargs)
