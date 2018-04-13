from django.db import models
from django.core.validators import RegexValidator


# Create your models here.


class CustomerInfo(models.Model):
    customer_number = models.CharField('代表者番号', validators=[RegexValidator('\d{6}')], max_length=6, unique=True)
    first_name = models.CharField('代表者氏名(姓)', max_length=15)
    second_name = models.CharField('代表者氏名(名)', max_length=15)
    first_name_kana = models.CharField('代表者氏名（セイ）', max_length=30)
    second_name_kana = models.CharField('代表者氏名（メイ）', max_length=30)
    zip_code = models.CharField('郵便番号', validators=[RegexValidator('\d{7}')], max_length=7, blank=True)
    address = models.CharField('住所', max_length=255)
    phone = models.CharField('電話番号', validators=[RegexValidator('\d{3,11}')], max_length=11)

    def __str__(self):
        return self.customer_number


class UserInfo(models.Model):
    customer = models.ForeignKey(CustomerInfo, on_delete=models.PROTECT)
    user_number = models.CharField('利用者番号', validators=[RegexValidator('[A-Z]{1}\d{6}')], max_length=7,unique=True)
    first_name = models.CharField('利用者氏名(姓)', max_length=15)
    second_name = models.CharField('利用者氏名(名)', max_length=15)
    first_name_kana = models.CharField('利用者氏名（セイ）', max_length=30)
    second_name_kana = models.CharField('利用者氏名（メイ）', max_length=30)
    age = models.IntegerField('年齢')
    height = models.IntegerField('身長')
    wight = models.IntegerField('体重')
    foot = models.CharField('足サイズ', max_length=4)
    memo = models.TextField('備考', max_length=255, null=True,blank=True)
    last_use_date = models.DateField('最終利用日',null=True)

    @classmethod
    def make_user_number(cls, customer_number):
        return "A" + customer_number

    def __str__(self):
        return self.user_number

class Rental(models.Model):
    rental_date = models.DateField('申込日')
    rental_start_date = models.DateField('レンタル開始日')
    rental_end_date = models.DateField('レンタル終了日', null=True)
    user = models.ForeignKey(UserInfo, on_delete=models.PROTECT)
    kind = models.CharField('レンタル種目', max_length=10)
    item_summary = models.CharField('レンタルセット内容', max_length=20)
    base_fee = models.IntegerField('基本合計金額')
    discount = models.IntegerField('割引金額', null=True)
    total_fee = models.IntegerField('合計金額')
    memo = models.TextField('備考', max_length=50, null=True)



class RentalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT)
    item_name = models.CharField('レンタル用品', max_length=20)
    item_id = models.CharField('レンタル品ID', max_length=10, null=True)


class RentalMenuKindMaster(models.Model):
    kind_id = models.CharField('レンタル種目ID',max_length=2,primary_key=True)
    kind_name = models.CharField('レンタル種目名', max_length=10)

    def __str__(self):
        return self.kind_name


class RentalMenuMaster(models.Model):
    kind = models.ForeignKey(RentalMenuKindMaster,on_delete=models.PROTECT)
    menu_name = models.CharField('レンタルセット内容',max_length=20)
    base_fee = models.IntegerField('基本合計金額')

    def __str__(self):
        return self.menu_name








