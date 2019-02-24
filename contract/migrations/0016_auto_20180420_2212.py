# Generated by Django 2.0.1 on 2018-04-20 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0015_auto_20180417_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalinfo',
            name='age',
            field=models.IntegerField(null=True, verbose_name='年齢'),
        ),
        migrations.AlterField(
            model_name='rentalinfo',
            name='discount',
            field=models.IntegerField(null=True, verbose_name='割引金額'),
        ),
        migrations.AlterField(
            model_name='rentalinfo',
            name='height',
            field=models.IntegerField(null=True, verbose_name='身長'),
        ),
        migrations.AlterField(
            model_name='rentalinfo',
            name='rental_end_date',
            field=models.DateField(null=True, verbose_name='レンタル終了日'),
        ),
        migrations.AlterField(
            model_name='rentalinfo',
            name='wight',
            field=models.IntegerField(null=True, verbose_name='体重'),
        ),
    ]
