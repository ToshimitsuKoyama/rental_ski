# Generated by Django 2.0.1 on 2018-02-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0005_auto_20180210_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='memo',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='備考'),
        ),
    ]
