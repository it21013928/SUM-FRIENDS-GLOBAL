# Generated by Django 3.2.9 on 2021-11-21 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_homepage_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
    ]
