from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    first_name = None
    last_name = None

    def __str__(self):
        return self.username


class Book(models.Model):
    name = models.CharField(max_length=200, default='')
    author = models.CharField(max_length=100, default='')
    mrp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} by {self.author}'


class BookOrder(models.Model):
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        User, related_name='customer', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return(self.customer.username)


class Bookmark(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} {self.book.name}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
