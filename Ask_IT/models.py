from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class UserAdditional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default='avatars/default_avatar.png')
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    numberOfResponses = models.IntegerField(default=0);

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class BestAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="bestanswer")
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + ' ' + self.answer.author.username


class LastAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="lastanswer")
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + ' ' + self.answer.author.username
