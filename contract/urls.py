
from django.urls import include, path
from django.views.generic.base import TemplateView
from .views import sample_view, NewCustomerView, NewRentalContractView, CustomerSearchView, EditCustomerView, \
    RentalInfoSearchView, EditRentalContractView, NewRentalTopView, DetailCustomerView

app_name = "contract"

urlpatterns = [
    path('new_customer/', NewCustomerView.as_view(), name='new_customer'),
    path('new_rental/<slug:customer_number>', NewRentalContractView.as_view(), name='new_rental'),
    path('search_customer/', CustomerSearchView.as_view(), name='search_customer'),
    path('edit_customer/<slug:customer_number>', EditCustomerView.as_view(), name='edit_customer'),
    path('search_rental/',RentalInfoSearchView.as_view(), name='search_rental'),
    path('edit_rental/<int:contract_id>', EditRentalContractView.as_view(), name="edit_rental"),
    path('new_rental_top/', NewRentalTopView.as_view(), name="new_rental_top"),
    path('detail_customer/<slug:customer_number>', DetailCustomerView.as_view(), name='detail_customer')
]
