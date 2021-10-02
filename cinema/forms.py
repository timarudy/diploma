from django.contrib.auth import forms
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Cinema, MyUser, Purchase, Session


class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ["username", ]

class BuyForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ["ticket_amount"]

class SessionAppendForm(ModelForm):
    class Meta:
        model = Session
        exclude = ["free_places"]

    def clean(self, *args, **kwargs):
        begins_at = self.cleaned_data.get("begins_at")
        ends_at = self.cleaned_data.get("ends_at")
        first_day = self.cleaned_data.get("first_day")
        last_day = self.cleaned_data.get("last_day")
        if begins_at >= ends_at:
            raise forms.ValidationError("Start Time Of the Session Can't Be Later Than the End Time")
        elif first_day > last_day:
            raise forms.ValidationError("the First Day Can't Be Later Than the Last Day")

class CinemaAppendForm(ModelForm):
    class Meta:
        model = Cinema
        fields = "__all__"