# Generated by Django 2.0.1 on 2018-04-13 15:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0012_auto_20180414_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_number', models.CharField(max_length=7, null=True, validators=[django.core.validators.RegexValidator('[A-Z]{1}\\d{6}')], verbose_name='利用者番号')),
                ('first_name', models.CharField(max_length=15, null=True, verbose_name='利用者氏名(姓)')),
                ('second_name', models.CharField(max_length=15, null=True, verbose_name='利用者氏名(名)')),
                ('first_name_kana', models.CharField(max_length=30, null=True, verbose_name='利用者氏名（セイ）')),
                ('second_name_kana', models.CharField(max_length=30, null=True, verbose_name='利用者氏名（メイ）')),
                ('age', models.IntegerField(null=True, verbose_name='年齢')),
                ('height', models.IntegerField(null=True, verbose_name='身長')),
                ('wight', models.IntegerField(null=True, verbose_name='体重')),
                ('foot', models.CharField(max_length=4, null=True, verbose_name='足サイズ')),
                ('rental_start_date', models.DateField(verbose_name='レンタル開始日')),
                ('rental_end_date', models.DateField(null=True, verbose_name='レンタル終了日')),
                ('kind', models.CharField(max_length=10, verbose_name='レンタル種目')),
                ('item_summary', models.CharField(max_length=20, verbose_name='レンタルセット内容')),
                ('base_fee', models.IntegerField(verbose_name='基本料金')),
                ('discount', models.IntegerField(null=True, verbose_name='割引金額')),
                ('total_fee', models.IntegerField(verbose_name='小計')),
                ('memo', models.TextField(max_length=50, null=True, verbose_name='備考')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contract.ContractInfo')),
            ],
        ),
        migrations.RemoveField(
            model_name='rental',
            name='customer',
        ),
        migrations.AlterField(
            model_name='rentalitem',
            name='rental',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contract.RentalInfo'),
        ),
        migrations.DeleteModel(
            name='Rental',
        ),
    ]