# Generated by Django 4.2 on 2024-05-19 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0013_alter_cours_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cours',
            name='description2',
            field=models.CharField(default='description', max_length=511),
        ),
    ]
