from django.db import models
from django.core.validators import RegexValidator
from django.forms.models import model_to_dict


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

    def to_dict(self):
        return model_to_dict(self)

    def __str__(self):
        return self.customer_number


class ContractInfo(models.Model):

    rental_date = models.DateField('レンタル日')
    customer = models.ForeignKey(CustomerInfo, on_delete=models.PROTECT)
    all_fee = models.IntegerField('金額')
    all_discount = models.IntegerField('割引金額', null=True, blank=True)
    total_fee = models.IntegerField('割引後金額')


class RentalMenuMaster(models.Model):
    kind_id = models.CharField('レンタル種目ID',max_length=2)
    kind_name = models.CharField('レンタル種目名', max_length=10)
    menu_name = models.CharField('レンタルセット内容',max_length=20)
    base_fee = models.IntegerField('基本金額')

    def __str__(self):
        return self.kind_name + "-" + self.menu_name


class RentalInfo(models.Model):
    contract = models.ForeignKey(ContractInfo, on_delete=models.PROTECT)
    user_number = models.CharField('利用者番号', validators=[RegexValidator('[A-Z]{1}\d{6}')], max_length=7)
    first_name = models.CharField('利用者氏名(姓)', max_length=15, blank=True)
    second_name = models.CharField('利用者氏名(名)', max_length=15, blank=True)
    first_name_kana = models.CharField('利用者氏名（セイ）', max_length=30, blank=True)
    second_name_kana = models.CharField('利用者氏名（メイ）', max_length=30, blank=True)
    age = models.IntegerField('年齢',null=True, blank=True)
    height = models.IntegerField('身長',null=True, blank=True)
    wight = models.IntegerField('体重',null=True, blank=True)
    foot = models.CharField('足サイズ', max_length=4,blank=True)
    rental_start_date = models.DateField('レンタル開始日')
    rental_end_date = models.DateField('レンタル終了日', null=True, blank=True)
    rental_menu = models.ForeignKey(RentalMenuMaster, on_delete=models.PROTECT)
    base_fee = models.IntegerField('基本料金')
    discount = models.IntegerField('割引金額', null=True, blank=True)
    subtotal_fee = models.IntegerField('小計')
    memo = models.TextField('備考', max_length=50, blank=True)

    def get_item_summary_display(self):
        return RentalMenuMaster.objects.filter(kind_id=self.item)


class RentalItem(models.Model):
    rental = models.ForeignKey(RentalInfo, on_delete=models.PROTECT)
    item_name = models.CharField('レンタル用品', max_length=20)
    item_id = models.CharField('レンタル品ID', max_length=10, blank=True)




