# Generated by Django 3.2.9 on 2021-11-20 20:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
