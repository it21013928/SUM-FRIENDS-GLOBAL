# Generated by Django 3.2.9 on 2021-12-14 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('home', '0008_contactpage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContactPage',
        ),
    ]
