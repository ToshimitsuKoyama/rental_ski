# Generated by Django 2.0.1 on 2018-05-01 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0019_auto_20180420_2341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentalinfo',
            old_name='total_fee',
            new_name='subtotal_fee',
        ),
    ]