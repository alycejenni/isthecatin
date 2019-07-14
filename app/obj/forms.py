from django import forms
from django.contrib.auth.forms import AuthenticationForm

from app.obj.models import Casualty, Highlight


class UserLogin(AuthenticationForm):
    username = forms.CharField(label="username", max_length=30, widget=forms.TextInput(attrs={
        "tabindex": 1
    }))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        "tabindex": 2
    }))


class NominateHighlight(forms.ModelForm):
    url = forms.URLField(required=True, widget=forms.HiddenInput(attrs={
        "class": "hidden-url"
    }))
    comment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "style": "width:100%"
    }))

    class Meta:
        model = Highlight
        fields = ["url", "comment"]


class CreateCasualty(forms.ModelForm):
    url = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "onkeyup": "refreshCaught()",
        "onchange": "refreshCaught()",
        "placeholder": "image url here",
        "class": "form-control"
    }))
    creature_type = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    creature_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    doa = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "class": "toggle-cat",
        "onchange": "checkDOA()"
    }))
    known_deceased = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "class": "toggle-cat"
    }))
    additional_image = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "onkeyup": "refreshAdditional()",
        "onchange": "refreshAdditional()",
        "placeholder": "image url here",
        "class": "form-control"
    }))
    guilty_cat = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "onkeyup": "refreshGuilty()",
        "onchange": "refreshGuilty()",
        "placeholder": "image url here",
        "class": "form-control"
    }))
    time_taken = forms.DateField(required=False, widget=forms.DateInput(attrs={
        "class": "form-control",
        "type": "date"
    }))

    class Meta:
        model = Casualty
        fields = ["url", "creature_type", "creature_name", "doa", "known_deceased", "additional_image", "guilty_cat",
                  "time_taken"]
