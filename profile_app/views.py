from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserCreateForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import (
    Profile,
)


# Create your views here.


@login_required
def current_profile(request):
    return render(request, 'profile_app/current_profile.html')


def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profile_app:login')
    else:
        form = UserCreateForm()
    return render(request, 'profile_app/create_profile.html', {'form': form})


def change_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # ------------------------ можно делать вот так вот, если у пользователя нет профиля!!! :)
        # profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=Profile.objects.get(user=user_form))
        # ---------------------------------------------------- и паковать джейсончик
        # if profile_form:
        #     json_data = {
        #         'id': profile_form.id,
        #         'user': user_form.id,
        #         'address': profile_form.address
        #     }
        # ---------------- или же вот так
        # try:
        #     profile_form = ProfileUpdateForm(request.POST, request.FILES,
        #       instance=Profile.objects.get(user=user_form))
        # except ObjectDoesNotExist as exception_alias:
        #     response = JsonResponse({'error': f'{exception_alias}'})
        #     response.status_code = 200
        #     return response
        # json_data = {
        #     'id': profile_form.id,
        #     'user': user_form.id,
        #     'address': profile_form.address
        # }
        # -----------------------------------------------------------------------------------
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been successfully updated!')
            return redirect('profile_app:current_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile_app/change_profile.html', context)

    # return JsonResponse({'profile': json_data})
