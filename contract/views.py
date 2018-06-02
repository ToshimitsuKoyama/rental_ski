from array import array
import collections
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from contract.forms import ContractForm, CustomerForm, RentalInfoForm, NewRentalFormSet, CustomerSearchForm, \
    RentalSearchForm, EditRentalFormSet
from contract.models import CustomerInfo, RentalInfo, RentalMenuMaster,ContractInfo
from django.views.generic.edit import FormView, CreateView, UpdateView, DeletionMixin
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

from django.forms.models import model_to_dict
from contract.utility import ModelSearchViewBase

# Create your views here.


@login_required
def sample_view(request):
    return HttpResponse('Hello World')


class NewCustomerView(CreateView):
    model = CustomerInfo
    template_name = 'contract/new_customer.html'
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('contract:new_rental', args=[self.object.customer_number])


class EditCustomerView(UpdateView, DeletionMixin):
    template_name = 'contract/edit_customer.html'
    form_class = CustomerForm

    model = CustomerInfo

    def post(self, request, *args, **kwargs):
        update_fix_btn_name = "update_fix_btn"
        delete_fix_btn_name = "delete_fix_btn"

        if delete_fix_btn_name in request.POST:
            return self.delete(request, *args, **kwargs)
        elif update_fix_btn_name in request.POST:
            return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('contract:edit_customer', args=[self.object.id])

    def form_valid(self, form):
        form.save()
        success_msg = "お客様情報を更新しました"
        return self.render_to_response(self.get_context_data(form=form, msg=success_msg))


class NewRentalContractView(FormView):
    template_name = 'contract/rental_contract_form.html'
    form_class = ContractForm

    customer_object = None
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg)
        self.customer_object = CustomerInfo.objects.get(pk=pk)
        return super().get(request, args, kwargs)

    def get_success_url(self):
        return reverse('contract:new_customer')

    def form_valid(self, form):
        ctx = self.get_context_data()
        rental_formset = ctx['inline']
        if rental_formset.is_valid() and form.is_valid():
            contract_model = form.save(commit=False)
            contract_model.customer = self.customer_object
            contract_model.save()

            for rental_form in rental_formset:
                rental_model = rental_form.save(commit=False)
                rental_model.contract = contract_model
                rental_model.save()

            return super().form_valid(form)

        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['form'] = ContractForm(self.request.POST)
            ctx['inline'] = NewRentalFormSet(self.request.POST)
        else:
            # 顧客情報をテンプレートへ連携
            contract_form_init = {
                "customer_number" : self.customer_object.customer_number,
                "customer_name" : self.customer_object.first_name + self.customer_object.second_name
            }
            ctx['form'] = ContractForm(initial=contract_form_init)
            ctx['inline'] = NewRentalFormSet(queryset=RentalInfo.objects.none())

        # メニューのリストをテンプレートへ連携
        menu_list = RentalMenuMaster.objects.all().values()
        ctx['rental_menu_list'] = list(menu_list)
        return ctx


class EditRentalContractView(FormView):
    template_name = 'contract/rental_contract_form.html'
    form_class = ContractForm

    rental_contract_object = None
    rental_info_query_set = None
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg)

        self.rental_contract_object = ContractInfo.objects.get(pk=pk)
        self.rental_info_query_set = RentalInfo.objects.filter(contract=self.rental_contract_object)

        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['form'] = ContractForm(self.request.POST)
            ctx['inline'] = EditRentalFormSet(self.request.POST)
        else:
            contract_form_init = {
                "customer_number" : self.rental_contract_object.customer.customer_number,
                "customer_name" : self.rental_contract_object.customer.first_name + self.rental_contract_object.customer.second_name
            }
            ctx['form'] = ContractForm(initial=contract_form_init, instance= self.rental_contract_object)
            ctx['inline'] = EditRentalFormSet(queryset=self.rental_info_query_set)

        # メニューのリストをテンプレートへ連携
        menu_list = RentalMenuMaster.objects.all().values()
        ctx['rental_menu_list'] = list(menu_list)
        return ctx


class CustomerSearchView(ModelSearchViewBase):

    template_name = 'contract/search_customer.html'
    model = CustomerInfo
    form_class = CustomerSearchForm

    def _get_input_filter_queryset(self):
        customer_list = super()._get_input_filter_queryset().values()

        queryset = []
        for customer in customer_list:
            customer_number = customer["customer_number"]
            contract = ContractInfo.objects.filter(customer__customer_number=[customer_number]).order_by('rental_date').first()
            if contract:
                customer.update({"last_date": contract.rental_date})

            queryset.append(customer)

        return queryset

    def _get_customer_detail_url(self, customer_number):
        return reverse('contract:edit_customer', args=[customer_number])


class RentalInfoSearchView(ModelSearchViewBase):

    template_name = 'contract/search_rental.html'
    model = RentalInfo
    form_class = RentalSearchForm


class NewRentalTopView(TemplateView):
    template_name = 'contract/new_rental_top.html'














