# Generated by Django 2.0.1 on 2018-05-01 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0020_auto_20180501_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contractinfo',
            old_name='discount',
            new_name='all_discount',
        ),
        migrations.RenameField(
            model_name='contractinfo',
            old_name='base_fee',
            new_name='all_fee',
        ),
    ]
