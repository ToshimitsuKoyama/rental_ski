
from django.urls import include, path
from django.views.generic.base import TemplateView
from .views import sample_view, NewCustomerView,NewRentalContractView,CustomerSearchView,EditCustomerView

app_name = "contract"

urlpatterns = [
    path('new/', NewCustomerView.as_view(), name='new_customer'),
    path('new_rental/<str:customer_number>', NewRentalContractView.as_view(), name='new_rental'),
    path('search/', CustomerSearchView.as_view(), name='customer_search'),
    path('edit/<int:pk>', EditCustomerView.as_view(), name='edit_customer'),
]
