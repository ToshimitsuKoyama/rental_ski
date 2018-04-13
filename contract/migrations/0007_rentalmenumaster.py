# Generated by Django 2.0.1 on 2018-02-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0006_auto_20180210_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalMenuMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=10, verbose_name='レンタル種目')),
                ('menu_name', models.CharField(max_length=20, verbose_name='レンタルセット内容')),
                ('base_fee', models.IntegerField(verbose_name='基本合計金額')),
            ],
        ),
    ]
