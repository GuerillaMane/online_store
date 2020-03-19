from django import forms


class PromoCodeApplyForm(forms.Form):
    code = forms.CharField()
