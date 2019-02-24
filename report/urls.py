from django.urls import include, path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('today/', TemplateView.as_view(template_name='report/today_report.html'), name='today_report'),
]
