# Generated by Django 4.2.8 on 2023-12-29 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(default='USD', max_length=3),
        ),
    ]
