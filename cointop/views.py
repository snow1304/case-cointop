"""Cointop views"""
import typing

import django.http
from coinapi_rest_v1 import restapi
from django import shortcuts, views
from django.contrib.auth import mixins
from django.contrib.auth import models as auth_models

from admin_cointop import settings
from cointop import forms, models

if typing.TYPE_CHECKING:
    from django.db.models import query


class Home(mixins.LoginRequiredMixin, views.View):
    _coinapi: "restapi.CoinAPIv1" = restapi.CoinAPIv1(settings.COIN_API_KEY)

    def get(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        return shortcuts.render(
            request,
            "cointop/home.html",
            {
                "alerts": self._get_user_alers(request.user),
                "alert_form": forms.AlertForm(),
            },
        )

    def post(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        """Handle alerts creation"""
        if not request.user.is_authenticated:
            return shortcuts.redirect("login")
        form = forms.AlertForm(request.POST)
        if form.is_valid():
            alert = form.save()
            alert.user.add(request.user)
            alert.save()
            return self.get(request)
        return shortcuts.render(
            request,
            "cointop/home.html",
            {
                "alerts": self._get_user_alers(request.user),
                "alert_form": form,
            },
        )

    def delete(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        """Delete an alert"""
        if not request.user.is_authenticated:
            return shortcuts.redirect("login")
        asset_id = self.request.GET.get("asset")
        if asset_id is None:
            return django.http.HttpResponse(status=400)
        alert = request.user.alerts.get(id=asset_id)
        request.user.alerts.remove(alert)
        return django.http.HttpResponse(status=200)

    def _get_user_alers(self, user) -> "query.QuerySet[models.Alert]":
        """Get user alerts"""
        return models.Alert.objects.filter(user=user)
