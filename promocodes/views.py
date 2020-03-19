from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import PromoCode
from .forms import PromoCodeApplyForm

# Create your views here.


@require_POST
def promocode_apply(request):
    now = timezone.now()
    form = PromoCodeApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            promocode = PromoCode.objects.get(
                code__exact=code,
                # check are codes match
                valid_from__lte=now,
                # check is less or equal date
                valid_to__gte=now,
                # check is greater or equal date
                is_active=True
            )
            request.session['promocode_id'] = promocode.id
        except PromoCode.DoesNotExist:
            request.session['promocode_id'] = None
    return redirect('cart:cart_detail')
