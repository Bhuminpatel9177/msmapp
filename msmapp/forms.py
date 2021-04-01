from django import forms

from .models import *


class EditProfile(forms.ModelForm):
    class Meta:
        model = Register
        fields = "__all__"