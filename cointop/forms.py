"""Forms"""
import typing

from django import forms

from cointop import models

AFM = typing.TypeVar("AFM", bound="AlertForm")


class AlertForm(forms.ModelForm):
    class Meta:
        model = models.Alert
        fields = ["asset", "high_low", "value"]

    def __init__(self: AFM, *args: typing.List, **kwargs: typing.Dict) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
