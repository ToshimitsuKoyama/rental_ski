from django import forms
from contract.models import CustomerInfo, ContractInfo, RentalInfo, RentalMenuMaster
import datetime
from django.forms import modelformset_factory, ModelChoiceField
from collections import OrderedDict
import json
from contract.utility import EmptyChoiceField,ModelSearchFormBase


class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ['customer_number', 'first_name', 'second_name',
                  'first_name_kana', 'second_name_kana', 'zip_code',
                  'address', 'phone']


class DetailCustomerForm(CustomerForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True


class ContractForm(forms.ModelForm):
    # customer_number = forms.CharField(label='顧客番号',
    #                                   widget=forms.TextInput(attrs={'readonly': 'readonly'})
    #                                   )
    customer_number = forms.CharField(label='顧客番号',
                                      disabled=True
                                      )
    customer_name = forms.CharField(label='顧客名',
                                    disabled=True
                                    )

    rental_date = forms.DateField(label='レンタル日', input_formats=('%Y/%m/%d',),
                                  initial=datetime.datetime.today().strftime("%Y/%m/%d"),
                                  widget=forms.TextInput(attrs={'class': "calender"})
                                  )

    all_fee = forms.IntegerField(label='料金',
                                 widget=forms.TextInput(attrs={'class':"input_number"})
                                 )

    all_discount = forms.IntegerField(label='割引', required=False,
                                      widget=forms.TextInput(attrs={'class':"input_number"})
                                      )

    total_fee = forms.IntegerField(label='合計',
                                   widget=forms.TextInput(attrs={'class':"input_number"})
                                   )

    class Meta:
        model = ContractInfo
        fields = ['customer_number', 'customer_name', 'rental_date', 'all_fee', 'all_discount','total_fee']


class RentalInfoForm(forms.ModelForm):

    rental_start_date = forms.DateField(label='レンタル開始日', input_formats=('%Y/%m/%d',),
                                        initial=datetime.datetime.today().strftime("%Y/%m/%d"),
                                        widget=forms.TextInput(attrs={'class': "calender"})
                                        )
    rental_end_date = forms.DateField(label='レンタル終了日', input_formats=('%Y/%m/%d',), required=False,
                                      widget=forms.TextInput(attrs={'class': "calender"})
                                      )

    base_fee = forms.IntegerField(label='基本料金',
                               widget=forms.TextInput(attrs={'class':"input_number"})
                               )

    discount = forms.IntegerField(label='割引', required=False,
                               widget=forms.TextInput(attrs={'class':"input_number"})
                               )

    subtotal_fee = forms.IntegerField(label='小計',
                                widget=forms.TextInput(attrs={'class':"input_number"})
                                )

    rental_menu = ModelChoiceField(label='レンタルメニュー', queryset=RentalMenuMaster.objects.all())

    class Meta:
        model = RentalInfo
        fields = ['user_number', 'first_name', 'second_name', 'first_name_kana','second_name_kana',
                  'age', 'height', 'wight', 'foot',
                  'rental_start_date', 'rental_end_date','rental_menu', 'base_fee',
                  'discount', 'subtotal_fee', 'memo']


NewRentalFormSet = modelformset_factory(model=RentalInfo, form=RentalInfoForm, extra=1)
EditRentalFormSet = modelformset_factory(model=RentalInfo, form=RentalInfoForm, extra=0)


class CustomerSearchForm(ModelSearchFormBase):

    model_cls = CustomerInfo

    customer_number = forms.CharField(label='代表者番号', required=False)
    first_name = forms.CharField(label='氏名',required=False,
                                 widget = forms.TextInput(
                                     attrs={'placeholder': '白根'})
                                 )
    second_name = forms.CharField(label='　',required=False)
    first_name_kana = forms.CharField(label='シメイ',required=False)
    second_name_kana = forms.CharField(label='　',required=False)


class RentalSearchForm(ModelSearchFormBase):
    model_cls = RentalInfo

    rental_start_date = forms.DateField(label='レンタル日付', required=False)
    contract__customer__customer_number = forms.CharField(label='代表者番号', required=False)
    contract__customer__first_name = forms.CharField(label='顧客名（姓）',required=False)
    contract__customer__second_name = forms.CharField(label='顧客名（名）',required=False)

