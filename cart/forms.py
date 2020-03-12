from django import forms

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 51)]


class CartAddForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=QUANTITY_CHOICES,
        coerce=int
    )
    # получаем введенные данные и преобразуем в int

    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
    # что делаем: обновляем или добавляем (hidden потому что пользователю это видеть не надо)
