# Generated by Django 5.0.6 on 2024-07-04 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0001_initial'),
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='trips',
            field=models.ManyToManyField(blank=True, related_name='trips', to='trips.trip'),
        ),
    ]
