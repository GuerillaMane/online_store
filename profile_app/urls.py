from django.urls import path
from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    create_user,
    current_profile,
    change_profile,
)


app_name = 'profile_app'


urlpatterns = [
    path('login/', LoginView.as_view(template_name='profile_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/profile/login'), name='logout'),
    path('create_profile/', create_user, name='create_profile'),
    path('current_profile/', current_profile, name='current_profile'),
    path('change_profile/', change_profile, name='change_profile'),

    path('api/', include('profile_app.api.urls')),
]
