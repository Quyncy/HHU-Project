from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import *
#########
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )
#########

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        exclude = ['date_joined','last_login',]

# class TutorProfileForm(forms.ModelForm):
#     class Meta:
#         model=TutorProfile
#         fields='__all__'

#         label = {
#             'user': _('Vorname'),
#             'student_id': _('ID'),
#             'kurs': _('Kurs'),
#             'arbeitsstunden': _('Arbeitsstunden'),
#             'anzahl_korrekturen': _('Anzahl Korrekturen'),
#         }
#         error_messages = {
#             'user':{
#                 'required': ('Vorname angeben')
#             }
#         }


class KursleiterForm(forms.ModelForm):
    class Meta:
        model = Kursleiter
        exclude = ['username','date_joined','last_login',]

class UserForm(forms.ModelForm):
    """ Bei Admin eingaben werden die fields ignoriert """
    class Meta:
        model = User
        exclude = ['username','date_joined','last_login',]

# class PersonAdmin(admin.ModelAdmin):
#     form = StudentForm

# class KursleiterProfileForm(forms.ModelForm):
#     class Meta:
#         model = KursleiterProfile
#         fields = '__all__'
#         label = {
#             'user': _('User'),
#             'kursleiter_id': _('Kursleiter ID'),
#         }


class DozentForm(forms.ModelForm):
    class Meta:
        model = Dozent
        fields = '__all__'
        labels = {
            'titel': _('Titel'),
            'vorname': _('Vorname'),
            'nachname': _('Nachname'),
        }
        error_messages = {
            'titel':{
                'required': _('Title has to be choosen')
            },
            'vorname':{
                'required': _('First name has to be entered')
            },
            'nachname': _('Last name has to be entered')
        },


class KursForm(forms.ModelForm):
    class Meta:
        model = Kurs
        fields = '__all__'
        # exclude=

        # labels := Bezeichnung
        labels = {
            'kurs_name': _('Kursname eingeben'),
            'beschreibung': _('Beschreibung eingegeben'),
            'dozent': _('Dozent eingeben'),
            'kursleiter': _('Kursleiter eingeben'),
            'semester': _('Semester eingegeben'),
        }
        error_messages = {
            fields : {
                'kurs_name': {
                    'required': _('Module name has to be entered')
                },
                'beschreibung': {
                    'required': _('Description has to be entered')
                },
                'dozent': {
                    'required': _('Dozent has to be entered')
                },
                'Kursleiter': {
                    'required': _('Teacher has to be entered')
                },
                'semester': {
                    'required': _('Semester has to be entered')
                },
            }
        }
