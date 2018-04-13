
from django.urls import include, path
from django.views.generic.base import TemplateView
from .views import sample_view, NewCustomerView,NewUserView,NewRentalContractView,get_user_list_ajax_api,get_user_info_ajax_api

urlpatterns = [
    path('new/', NewCustomerView.as_view(), name='new_customer'),
    path('new_user/<str:customer_number>', NewUserView.as_view(), name='new_user'),
    path('new_rental/<str:customer_number>', NewRentalContractView.as_view(), name='new_rental'),
    path('new_rental/api/get_user_list', get_user_list_ajax_api, name='api_user_list'),
    path('new_rental/api/get_user_info', get_user_info_ajax_api, name='api_user_info'),
]
