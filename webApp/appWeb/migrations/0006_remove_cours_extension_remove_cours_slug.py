# Generated by Django 4.2 on 2024-05-05 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0005_alter_cours_contenutext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cours',
            name='extension',
        ),
        migrations.RemoveField(
            model_name='cours',
            name='slug',
        ),
    ]