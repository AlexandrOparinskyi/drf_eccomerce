# Generated by Django 5.1.3 on 2024-12-24 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['-id']},
        ),
    ]
