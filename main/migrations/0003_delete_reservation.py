# Generated by Django 5.0.1 on 2024-03-13 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_reservation_tourist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reservation',
        ),
    ]