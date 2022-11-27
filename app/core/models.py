from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from django.core.mail import send_mail
from django.conf import settings

import uuid

def send_password_mail(email, token):
    subject = 'HHU System - Passwort.'
    message = f'Willkommen im HHU System, mit dem folgenden Link können Sie ihr Passwort setzen: http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def setPassword(email):
    """ Funktion zum versenden des Passworts """
    try:
        if email:
            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile = Profile.objects.get(user=user)
            profile.password_token = token
            profile.save()
            send_password_mail(profile.user.email, token)

    except Exception as e:
        print(e)


class MyUserManager(BaseUserManager):
    def create_user(self, email, vorname, nachname, password=None, **extrafields):

        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_active', True)
        extrafields.setdefault('is_staff', True)

        if not email:
            raise ValueError("Benutzer benötigt eine Email")

        # password = User.objects.make_random_password()  # random Passwort generieren
        if password is not None:
            user = self.model(
                email=self.normalize_email(email),
                vorname=vorname,
                nachname=nachname,
                **extrafields
                )
            user.set_password(password)
            user.save()
        else:
            password = User.objects.make_random_password()
            user = self.model(
                email=self.normalize_email(email),
                vorname=vorname,
                nachname=nachname,
                **extrafields
                )
            user.set_password(password)
            user.save()
            setPassword(email)  # oben definierte Funktion
        return user

    def create_superuser(self, email, vorname, nachname, password, **extrafields):
        if not email:
            raise ValueError("Benutzer benötigt eine Email")

        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_active', True)
        extrafields.setdefault('is_staff', True)

        user = self.create_user(
            email,
            vorname,
            nachname,
            password,
            **extrafields,
        )
        user.save(using=self.db)
        return user


###############
# Beim hinzufügen der Daten wird die Rolle als admin zugewiesen
class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        TUTOR = "TUTOR", 'Tutor'
        KURSLEITER = "KURSLEITER", 'Kursleiter'

    base_user = Role.ADMIN

    # Welche Rolle hat der User
    role = models.CharField(("Rolle"), max_length=10, choices=Role.choices, default=base_user)
    vorname = models.CharField(max_length=255, blank=True)
    nachname = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_published = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['vorname', 'nachname',]

    objects = MyUserManager()

    class Meta:
        verbose_name_plural = "Benutzer"

    def save(self, *args, **kwargs):
        if self.id:
            self.role = self.base_user
            # email senden verifizieren active auf True setzen und
            # passwort setzen
            print(self.role)
        return super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_token = models.CharField(max_length=50) ##################
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.vorname} {self.user.nachname}'


class KursleiterManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.KURSLEITER)


class TutorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TUTOR)


class Dozent(models.Model):
    """Dozenten im System"""
    TITEL_CHOICES = [
        ('Prof.','Prof.'),
        ('Dr.', 'Dr.'),
    ]

    title = models.CharField(max_length=5, choices = TITEL_CHOICES, default='Prof.')  # Auswahl Prof., Dr., Wiss. Mitarbeiter
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Dozenten"

    def __str__(self):
        return f"{self.title} {self.vorname} {self.nachname}"


class Kurs(models.Model):
    """Kurse im System"""
    # field_of_study = Naturwissenschaften, Rechtswissenschaft???
    kurs_name = models.CharField(max_length=50)
    beschreibung = models.TextField(blank=True, null=True)
    ref_id = models.CharField(max_length=100)
    ass_id = models.CharField(max_length=100)
    dozent = models.ForeignKey(Dozent, on_delete=models.CASCADE)

    SEMESTER_CHOICES = [
        ('WS', 'Wintersemester'),   # 'WS'/'SS' wird in die Datenbank gespeichert und Wintersemester oder Sommersemester wird User angezeigt
        ('SS', 'Sommersemester'),
    ]

    semester = models.CharField(
        max_length=3,
        choices=SEMESTER_CHOICES,
        default='',
    )

    class Meta:
        verbose_name_plural = "Kurse"

    def __str__(self):
        return f"{self.kurs_name}"


class Tutor(User):
    """Tutoren im System"""
    base_user = User.Role.TUTOR
    kurs_name = models.ForeignKey(Kurs, on_delete=models.CASCADE, null=True)
    arbeitsstunden = models.FloatField(default=0)
    tutor_id = models.CharField(max_length=30)  # matrikelnummer

    tutor = TutorManager()

    @property
    def more(self):
        return self.tutorprofile

    class Meta:
        verbose_name_plural = "Tutoren"


class Kursleiter(User):
    """Kursleiter im System"""
    base_user = User.Role.KURSLEITER
    kurs_name = models.ForeignKey(Kurs, on_delete=models.CASCADE, null=True, blank=True)

    kursleiter = KursleiterManager()

    @property
    def more(self):
        return self.kursleiterprofile

    class Meta:
        verbose_name_plural = "Kursleiter"


# wartet auf ein Signal, sobald ein User gespeichert wird ein Profil erstellt
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Tutor)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Kursleiter)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=Tutor)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "TUTOR":
#         Tutor.objects.create(user=instance)
#         # profile.objects.create(user=instance)

# @receiver(post_save, sender=Kursleiter)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "TUTOR":
#         Kursleiter.objects.create(user=instance)
#         # Profile.objects.create(user=instance)

# # class Abgaben(models.Model):
# #     tutor = models.ForeignKey()
# #     korrektur = models.TextField()