"""
URL configuration for cointop project.
"""
from django import urls

from cointop import views

urlpatterns: list[urls.URLPattern] = [
    urls.path("", views.Home.as_view(), name="homepage"),
]
