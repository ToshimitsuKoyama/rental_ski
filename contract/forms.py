from django import forms
from contract.models import CustomerInfo, UserInfo, Rental, RentalMenuMaster, RentalMenuKindMaster
import datetime
from django.forms import modelformset_factory
from collections import OrderedDict
import json


class NewContractForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ['customer_number', 'first_name', 'second_name',
                  'first_name_kana', 'second_name_kana', 'zip_code',
                  'address', 'phone']


class NewUserForm(forms.ModelForm):
    user_number = forms.CharField(label='利用者番号',
                                  # widget=forms.TextInput(attrs={'readonly': 'readonly'})
                                  )

    class Meta:
        model = UserInfo
        fields = ['user_number', 'first_name', 'second_name', 'first_name_kana',
                  'second_name_kana', 'age', 'height', 'wight', 'foot', 'memo']


NewUserFormSet = modelformset_factory(UserInfo,form=NewUserForm,extra=1)


class NewRentalContractForm(forms.ModelForm):

    user = NewUserForm()

    rental_date = forms.DateField(label='申込日', input_formats=('%Y/%m/%d',),
                                  initial = datetime.datetime.today().strftime("%Y/%m/%d"),
                                  widget=forms.TextInput(attrs={'class':"calender"})
                                  )

    rental_start_date = forms.DateField(label='レンタル開始日', input_formats=('%Y/%m/%d',),
                                        initial = datetime.datetime.today().strftime("%Y/%m/%d"),
                                        widget=forms.TextInput(attrs={'class': "calender"})
                                        )
    rental_end_date = forms.DateField(label='レンタル終了日', input_formats=('%Y/%m/%d',),
                                      widget=forms.TextInput(attrs={'class': "calender"})
                                      )

    base_fee = forms.CharField(label='基本料金',
                               widget=forms.TextInput(attrs={'class':"input_number"})
                               )

    discount = forms.CharField(label='割引',
                               widget=forms.TextInput(attrs={'class':"input_number"})
                               )

    total_fee = forms.CharField(label='合計金額',
                                widget=forms.TextInput(attrs={'class':"input_number"})
                                )

    kind = forms.ModelChoiceField(label='レンタル種目',
                                  widget=forms.Select(),queryset=RentalMenuKindMaster.objects.all(),
                                  empty_label="選択してください")

    item_summary = forms.ModelChoiceField(label='レンタルニュー',
                                          widget=forms.Select(),queryset=RentalMenuMaster.objects.all(),
                                          empty_label= "選択してください")

    class Meta:
        model = Rental
        fields = ['rental_date', 'rental_start_date', 'rental_end_date',
                  'kind', 'item_summary', 'base_fee',
                  'discount', 'total_fee', 'memo']


NewRentalContractFormSet = modelformset_factory(Rental,form=NewRentalContractForm,extra=1)
