# Generated by Django 3.0.7 on 2020-06-25 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200625_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='timestamp',
            field=models.IntegerField(default=1593120502.800134),
        ),
    ]