# Generated by Django 3.1.4 on 2021-01-13 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercisesdetails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisesdetails',
            name='volume',
            field=models.IntegerField(default=0),
        ),
    ]