from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
)

# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    # login_url = ''
    template_name = 'shop/base.html'
