from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail
from django.conf import settings
import uuid

from .forms import LoginForm
from core.forms import *

def send_password_mail(email, token):
    subject = 'HHU System - Passwort.'
    message = f'Willkommen im HHU System, mit dem folgenden Link können Sie ihr Passwort setzen: http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password') # passwort hashen?

            user = authenticate(request, email = email , password = password)

            if not email or not password:
                messages.success(request, 'Email und Password benötigt.')
                return redirect('login')

            if user is not None:
                login(request , user)
                return redirect('/')

            if user is None:
                messages.success(request, 'User not found or wrong password.')
                return redirect('login')

            return redirect('ok')

    except Exception as e:
        print(e)

    return render(request , 'user/login.html')


def changePassword(request, token):
    context = {}
    try:
        User = get_user_model()
        profile = Profile.objects.get(password_token=token)
        context = {'user_id': profile.user.id}

        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = profile.user.id

            if user_id is None:
                messages.success(request, 'Keinen Eintrag gefunden.')
                return redirect(f'change-password/{token}') ##### ---------


            if new_password != confirm_password:
                messages.success(request, 'Passwort nicht identisch. Bitte versuchen Sie es noch einmal')
                return redirect(f'change-password/{token}')

            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

            return redirect('ok')
    except Exception as e:
        print(e)

    return render(request, 'user/change-password.html', context)


def setPassword(request):
    try:
        User = get_user_model()
        if request.method == "POST":
            email = request.POST.get('email')
            if not User.objects.get(email=email):
                messages.succes(request, 'Kein Benutzer mit dieser Email vorhanden')
                return redirect('forget-pasword')

            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile = Profile.objects.get(user=user)
            profile.password_token = token
            profile.save()
            # Email wird verschickt
            send_password_mail(profile.user.email, token)

            messages.success(request, 'Die Email wurde versendet.')
            return redirect('set-password')

    except Exception as e:
        print(e)

    return render(request, 'user/set-password.html')

def register(request):
    User = get_user_model()
    try:
        if request.method == "POST":
            email = request.POST.get['email']
            password = request.POST.get['password']

            try:
                if user.objects.get(email=email).first():
                    messages.succes(request, 'Diese E-Mail ist bereits vergeben.')
                    return redirect('user/register')

                user = User(email=email)
                user.set_password(password)


            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

    return render(request, 'user/register.html')


def logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def Home(request):
    return render(request , 'user/index.html')


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#         user = authenticate(request,
#                             email = data['email'],
#                             password = data['password'])
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('admin'))
#             else:
#                 return HttpResponse('Benutzer nicht vorhanden.')
#         else:
#             return HttpResponse('Passwort oder Email falsch.') # redirect zum login
#     else:
#         form = LoginForm()
#     return render(request, 'user/login.html', {'form': form})


def dozent(request):
    dozent_form = DozentForm()
    # error_message = ""
    if request.POST:
        dozent_form = DozentForm(request.POST)

        if dozent_form.is_valid():
            dozent_form.save()
            return redirect(reverse('ok'))

    context={'form':dozent_form, }
    return render(request, 'user/dozent.html', context)


def kurs(request):
    kurs_form = KursForm()

    if request.POST:
        kurs_form = KursForm(request.POST)

        if kurs_form.is_valid():
            kurs_form.save()
            return redirect(reverse('ok'))

    context = {'form': kurs_form, }
    return render(request, 'user/form.html', context)


def tutor(request):
    tutor_form = TutorForm()

    if request.POST:
        tutor_form = TutorForm(request.POST)

        if tutor_form.is_valid():
            tutor_form.save()
            return redirect(reverse('ok'))

    context={"form":tutor_form}
    return render(request, 'user/form.html', context)


def kursleiter(request):
    kursleiter_form = KursleiterForm()

    if request.POST:
        kursleiter_form = KursleiterForm(request.POST)

        if kursleiter_form.is_valid():
            kursleiter_form.save()
            return redirect(reverse('ok'))

    context={"form":kursleiter_form}
    return render(request, 'user/form.html', context)


def user(request):
    user_form = UserForm()

    if request.POST:
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('ok'))

    context={"form":user_form}
    return render(request, 'user/form.html', context)


# Ok-Seiten zum erfolreichen gespeichern
def ok(request):
    context={}
    return render(request, 'user/ok.html', context)


def profile(request):
    context = {}
    return render(request, 'user/form.html', context)