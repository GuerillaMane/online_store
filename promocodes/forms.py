from django import forms
from .models import PromoCode


class PromoCodeApplyForm(forms.Form):
    code = forms.CharField()


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = '__all__'
