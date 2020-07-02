from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class UserAdditional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class BestAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + ' ' + self.answer.author.username
