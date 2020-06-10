from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserAdditional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    # def __str__(self):
    #     return self.avatar


class Category(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE)

# tabela wątek -> odnośnik do kategorii i osoby i inne pierdoły
# tabela post (odpowiedź)
