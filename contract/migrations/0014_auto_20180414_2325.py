# Generated by Django 2.0.1 on 2018-04-14 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0013_auto_20180414_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalmenumaster',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rentalmenumaster',
            name='kind_id',
            field=models.CharField(max_length=2, verbose_name='レンタル種目ID'),
        ),
    ]