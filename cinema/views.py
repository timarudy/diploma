from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import *
from django.shortcuts import redirect
from .forms import BuyForm, CinemaAppendForm, RegisterForm, SessionAppendForm
from datetime import date


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/homepage/'


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.money = 10000
        obj.save()
        return super().form_valid(form=form)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/homepage/'
    login_url = '/login/'


class SessionListView(ListView):
    model = Session
    template_name = 'homepage.html'


class PurchasesListView(ListView):
    model = Purchase
    template_name = "purchases.html"


class SessionUpdate(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    template_name = "session_update.html"
    model = Session
    fields = ["ticket_price", "cinema", "first_day", "last_day", "begins_at", "ends_at"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.free_places = obj.cinema.size
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return "/homepage/"


class CinemaAppend(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = CinemaAppendForm
    template_name = "add_cinema.html"
    success_url = '/homepage/'


class SessionAppend(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = SessionAppendForm
    template_name = "add_session.html"
    success_url = '/homepage/'

    def form_valid(self, form):
        try:
            obj = form.save(commit=False)
            obj.free_places = obj.cinema.size
            obj.save()
            return redirect(self.get_success_url())
        except NotCorrectTime:
            return messages.error(self.request, "???? ???????????? ?????????? ?????? ???????? ??????????")
        finally:
            return super().form_valid(form)

    def get_success_url(self):
        return "/homepage/" 


class TicketBuy(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = BuyForm
    template_name = "purchase.html"

    def form_valid(self, form):
        try:
            purchase = form.save(commit=False)
            purchase.user = self.request.user
            purchase.ticket = Session.objects.get(pk=self.kwargs["pk"])
            purchase.save()
            return redirect(self.get_success_url())
        except NotEnoughMoney:
            return messages.error(self.request, "?? ?????? ???????????????????????? ??????????")
        except CannotBeZero:
            return messages.error(self.request, "?????????? ?????????????? ?????????? ????????-???? ???????? ??????????????")
        except NotEnoughTickets:
            return messages.error(self.request, "???????????????????????? ????????")
        finally:
            return redirect(f"/homepage/ticket-purchase/{self.kwargs['pk']}")

    def get_success_url(self):
        return "/homepage/"