"""Middlewares"""
import typing

from django.contrib.auth import decorators

if typing.TYPE_CHECKING:
    from django import http

LRM = typing.TypeVar("LRM", bound="LoginRequiredMiddleware")
_AUTHORIZED_RESOURCES: typing.Set[str] = {
    "/login",
    "/logout",
}


def login_exempt(view: typing.Callable) -> typing.Callable:
    view.login_exempt = True
    return view


class LoginRequiredMiddleware:
    """Middleware to ensure login before accessing website"""

    def __init__(self: LRM, get_response: typing.Callable) -> None:
        """Init login middleware"""
        self.get_response = get_response

    def __call__(self: LRM, request: "http.HttpRequest") -> "http.HttpResponse":
        return self.get_response(request)

    def process_view(
        self: LRM,
        request: "http.HttpRequest",
        view_func: typing.Callable,
        view_args: typing.List,
        view_kwargs: typing.Dict,
    ) -> typing.Optional["http.HttpResponseRedirect"]:
        if getattr(view_func, "login_exempt", False):
            return None

        if request.path in _AUTHORIZED_RESOURCES:
            return None

        if request.user.is_authenticated:
            return None

        return decorators.login_required(view_func)(request, *view_args, **view_kwargs)
