# Generated by Django 3.0.6 on 2020-07-02 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ask_IT', '0010_auto_20200702_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
