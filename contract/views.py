from array import array
import collections
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from contract.forms import ContractForm, CustomerForm, NewRentalForm, NewRentalFormSet, CustomerSearchForm
from contract.models import CustomerInfo, RentalInfo, RentalMenuMaster,ContractInfo
from django.views.generic.edit import FormView, CreateView, UpdateView, DeletionMixin
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin

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
    template_name = 'contract/new_rental_contract.html'
    form_class = ContractForm

    def get_success_url(self):
        return reverse('contract:new_customer')

    def form_valid(self, form):
        ctx = self.get_context_data()
        rental_formset = ctx['inline']
        if rental_formset.is_valid() and form.is_valid():
            contract_model = form.save(commit=False)
            contract_model.customer = CustomerInfo.objects.get(customer_number=form.cleaned_data["customer_number"])
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
            number = self.kwargs['customer_number']
            customer_info = CustomerInfo.objects.get(customer_number=number)
            contract_form_init = {
                "customer_number" : customer_info.customer_number,
                "customer_name" : customer_info.first_name + customer_info.second_name
            }
            ctx['form'] = ContractForm(initial=contract_form_init)
            ctx['inline'] = NewRentalFormSet(queryset=RentalInfo.objects.none())

        # メニューのリストをテンプレートへ連携
        item_summary_list = RentalMenuMaster.objects.all().values()
        ctx['item_summary_list'] = list(item_summary_list)
        return ctx


class CustomerSearchView(ListView):
    KEY_SEARCH_POST = 'search-post'

    template_name = 'contract/customer_search.html'
    model = CustomerInfo
    paginate_by = 5

    def get_queryset(self):

        queryset = []
        if self.request.session.has_key(self.KEY_SEARCH_POST):
            queryset = self._get_input_filter_queryset()

        return queryset

    def post(self, request, *args, **kwargs):
        self.request.session[self.KEY_SEARCH_POST] = self.request.POST
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self._is_search_post_info_del():
            del self.request.session[self.KEY_SEARCH_POST]
        return super().get(request, *args, **kwargs)

    def _is_search_post_info_del(self):
        if self.request.method == 'GET' \
                and "page" not in self.request.GET \
                and self.request.session.has_key(self.KEY_SEARCH_POST):

            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            search_form = CustomerSearchForm(self.request.POST)
        else:
            search_form = CustomerSearchForm()

        ctx['form'] = search_form
        return ctx

    def _get_input_filter_queryset(self):
        search_form = CustomerSearchForm(self.request.session[self.KEY_SEARCH_POST])
        customer_list = search_form.get_filter_queryset().order_by('customer_number').values()

        queryset = []
        for customer in customer_list:
            customer_number = customer["customer_number"]
            customer.update({"detail_url": self._get_customer_detail_url(customer_number)})
            contract = ContractInfo.objects.filter(customer__customer_number=[customer_number]).order_by('rental_date').first()
            if contract:
                customer.update({"last_date": contract.rental_date})

            queryset.append(customer)

        return queryset

    def _get_customer_detail_url(self, customer_number):
        return ""


class ContractSearchView(ListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            search_form = CustomerSearchForm(self.request.POST)
        else:
            search_form = CustomerSearchForm()

        ctx['form'] = search_form
        return ctx






