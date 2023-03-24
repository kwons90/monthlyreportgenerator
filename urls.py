from django.urls import path
from report_generator.views import generate_report_view

urlpatterns = [
    path('generate_report/', generate_report_view, name='generate_report'),
]