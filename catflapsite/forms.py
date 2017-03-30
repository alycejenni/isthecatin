from django import forms
from .models import Casualty

class CreateCasualty(forms.ModelForm):
    url = forms.CharField(required = False, widget=forms.TextInput(attrs={"onkeyup": "refreshCaught()", "onchange": "refreshCaught()"}))
    creature_name = forms.CharField(required = False)
    doa = forms.BooleanField(required = False, widget = forms.CheckboxInput(attrs = {"class": "toggle-cat", "onchange": "checkDOA()"}))
    known_deceased = forms.BooleanField(required = False, widget = forms.CheckboxInput(attrs = { "class": "toggle-cat"}))
    additional_image = forms.CharField(required = False,
        widget = forms.TextInput(attrs = { "onkeyup": "refreshAdditional()", "onchange": "refreshAdditional()" }))
    guilty_cat = forms.CharField(required = False,
        widget = forms.TextInput(attrs = { "onkeyup": "refreshGuilty()", "onchange": "refreshGuilty()" }))
    class Meta:
        model = Casualty
        fields = ["url", "creature_type", "creature_name", "doa", "known_deceased", "additional_image", "guilty_cat", "time_taken"]