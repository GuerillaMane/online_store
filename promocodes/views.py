from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.urls import reverse_lazy
from .models import PromoCode
from .forms import (
    PromoCodeApplyForm,
    PromoCodeForm
)
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView
)

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


class PromoList(ListView):
    template_name = 'promocodes/promocode_list.html'
    model = PromoCode
    context_object_name = 'promo_list'


class PromoCreate(CreateView):
    template_name = 'promocodes/promocode_create.html'
    model = PromoCode
    form_class = PromoCodeForm


class PromoDelete(DeleteView):
    model = PromoCode
    success_url = reverse_lazy('promocodes:promo_list')
    template_name = 'shop/confirm_delete.html'


class PromoDetail(DetailView):
    template_name = 'promocodes/promocode_detail.html'
    model = PromoCode
    context_object_name = 'promocode'


class PromoUpdate(UpdateView):
    template_name = 'promocodes/promocode_create.html'
    model = PromoCode
    form_class = PromoCodeForm
