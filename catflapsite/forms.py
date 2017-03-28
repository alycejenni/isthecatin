from django import forms
from .models import Casualty

class CreateCasualty(forms.ModelForm):
    class Meta:
        model = Casualty
        fields = ["url", "creature_type", "creature_name", "doa", "known_deceased", "additional_image", "guilty_cat"]