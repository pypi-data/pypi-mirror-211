# Generated by Django 4.1 on 2022-12-04 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_authcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='partial',
            field=models.IntegerField(default=0, verbose_name='Parcial'),
        ),
        migrations.AddField(
            model_name='task',
            name='total',
            field=models.IntegerField(default=0, verbose_name='Total'),
        ),
    ]
