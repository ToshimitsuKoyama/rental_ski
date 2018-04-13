from array import array

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from contract.forms import NewContractForm, NewUserForm, NewUserFormSet, NewRentalContractForm,NewRentalContractFormSet
from contract.models import CustomerInfo, UserInfo, Rental, RentalMenuMaster
from django.views.generic.edit import FormView,CreateView

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

from django.forms.models import model_to_dict

# Create your views here.


@login_required
def sample_view(request):
    return HttpResponse('Hello World')


class NewCustomerView(CreateView):
    model = CustomerInfo
    template_name = 'contract/new_customer.html'
    form_class = NewContractForm

    def get_success_url(self):
        return reverse('new_rental', args=(self.object.customer_number,))


class NewUserView(CreateView):
    model = UserInfo
    template_name = 'contract/new_user.html'
    form_class = NewUserForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 代表者番号をテンプレートへ連携
        number = self.kwargs['customer_number']
        ctx['customer'] = CustomerInfo.objects.get(customer_number=number)

        # 利用者番号を初期値に格納
        ctx['form'].initial['user_number']=UserInfo.make_user_number(ctx['customer'].customer_number)
        return ctx

    def get_success_url(self):
        return reverse('new_rental', args=(self.object.user_number,))

    def post(self, request, *args, **kwargs):
        self.object = None # BaseCreateViewの記載よりコピー
        form = NewUserForm(request.POST)
        if form.is_valid():
            user_model = form.save(commit=False)
            user_model.customer = CustomerInfo.objects.get(customer_number=self.kwargs['customer_number'])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class NewRentalContractView(CreateView):
    model = Rental
    template_name = 'contract/new_rental_contract.html'
    form_class = NewRentalContractForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = NewRentalContractForm(request.POST)
        if form.is_valid():
            rental_contract_model = form.save(commit=False)
            rental_contract_model.user = UserInfo.objects.get(user_number=self.kwargs['user_number'])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 顧客情報をテンプレートへ連携
        number = self.kwargs['customer_number']
        ctx['customer'] = CustomerInfo.objects.get(customer_number=number)

        # 利用者情報のformをテンプレートへ連携
        ctx['rental_form_set'] = NewRentalContractFormSet(queryset=Rental.objects.none())
        ctx['user_form_set'] = NewUserFormSet(queryset=UserInfo.objects.none())

        # メニューのリストをテンプレートへ連携
        item_summary_list = RentalMenuMaster.objects.all().values('id','menu_name','base_fee','kind__kind_id')
        ctx['item_summary_list'] = list(item_summary_list)
        return ctx


def get_user_list_ajax_api(request):
    if request.is_ajax():
        if request.method == 'GET':
            customer_id = request.GET.get('customer_id')
            user_list = list(UserInfo.objects.filter(customer__customer_number=customer_id).values('user_number','first_name','second_name'))

            d = {
                'user_list': user_list
            }
            return JsonResponse(d)


def get_user_info_ajax_api(request):
    if request.is_ajax():
        if request.method == 'GET':
            user_number = request.GET.get('user_number')
            try:
                user_info = model_to_dict(UserInfo.objects.get(user_number=user_number))
                d = {
                    'user_info': user_info
                }
                return JsonResponse(d)

            except MultipleObjectsReturned:
                print("exception error MultipleObjectsReturned")

            except ObjectDoesNotExist:
                print("exception error ObjectDoesNotExist")










