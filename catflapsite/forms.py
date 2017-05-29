from django import forms
from .models import Casualty
from django.contrib.auth.forms import AuthenticationForm


class UserLogin(AuthenticationForm):
    username = forms.CharField(label="username", max_length=30, widget=forms.TextInput(attrs={
        "tabindex": 1
        }))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        "tabindex": 2
        }))


class CreateCasualty(forms.ModelForm):
    url = forms.CharField(required = False, widget = forms.TextInput(
        attrs = {
            "onkeyup": "refreshCaught()",
            "onchange": "refreshCaught()",
            "placeholder": "image url here",
            "class": "form-control"
            }))
    creature_type = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control"
        }))
    creature_name = forms.CharField(required = False, widget = forms.TextInput(attrs = {
        "class": "form-control"
        }))
    doa = forms.BooleanField(required = False,
                             widget = forms.CheckboxInput(attrs = {
                                 "class": "toggle-cat",
                                 "onchange": "checkDOA()"
                                 }))
    known_deceased = forms.BooleanField(required = False,
                                        widget = forms.CheckboxInput(attrs = {
                                            "class": "toggle-cat"
                                            }))
    additional_image = forms.CharField(required = False,
                                       widget = forms.TextInput(attrs = {
                                           "onkeyup": "refreshAdditional()",
                                           "onchange": "refreshAdditional()",
                                           "placeholder": "image url here",
                                           "class": "form-control"
                                           }))
    guilty_cat = forms.CharField(required = False,
                                 widget = forms.TextInput(
                                     attrs = {
                                         "onkeyup": "refreshGuilty()",
                                         "onchange": "refreshGuilty()",
                                         "placeholder": "image url here",
                                         "class": "form-control"
                                         }))
    time_taken = forms.DateField(required = False,
                                 widget = forms.DateInput(
                                     attrs = {
                                         "class": "form-control",
                                         "type": "date"
                                         }
                                     ))

    class Meta:
        model = Casualty
        fields = ["url", "creature_type", "creature_name", "doa", "known_deceased", "additional_image", "guilty_cat",
                  "time_taken"]
