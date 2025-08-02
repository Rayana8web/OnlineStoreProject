from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm

from .forms import MyUserRegisterForm, MyUserLoginForm
#newstart
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from product.models import Estate

from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
#finish
def user_register_view(request):
    if request.method=='POST':
        form = MyUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно создали аккаунт')
            return redirect('index')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')



    else:
        form = MyUserRegisterForm()

    return render(request, 'register.html', {'form': form})

def user_login_view(request):
    if request.method=='POST':
        form=MyUserLoginForm(request.POST)
        if form.is_valid ():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data ['password']

            user = authenticate(request, username=user_email, password=user_password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('index')
        messages.error(request, 'Неверный email или пароль')

    form = MyUserLoginForm()
    return render(request, 'login.html', {'form': form})

#newstart
def user_logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')




@login_required
def favorites_view(request):
    user = request.user
    liked_ads = user.liked_ads.all()
    return render(request, 'ads/favorites.html', {'liked_ads': liked_ads})








def verify_otp_view(request):
    user_id = request.session.get('pre_2fa_user')
    user = get_object_or_404(MyUser, pk=user_id)

    if request.method == 'POST':
        code = request.POST.get('otp')
        if user.is_otp_valid(code):
            login(request, user)
            del request.session['pre_2fa_user']
            return redirect('index')
        messages.error(request, 'Неверный или просроченный код.')

    return render(request, 'verify_otp.html', {})

def resend_otp_view(request):
    user_id = request.session.get('pre_2fa_user')
    user = get_object_or_404(MyUser, pk=user_id)

    code = user.generate_otp()
    send_mail(
        'Ваш новый код подтверждения',
        f'Ваш новый код: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    messages.info(request, 'Код отправлен повторно.')
    return redirect('verify_otp')

#finish




