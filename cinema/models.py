from django.utils import timezone
from cinema.my_exeptions import CannotBeZero, NotCorrectTime, NotEnoughMoney, NotEnoughTickets
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


class MyUser(AbstractUser):
    money = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.username
    

class Cinema(models.Model):
    name = models.CharField(max_length=20, verbose_name="name of cinema")
    size = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="amount of places")

    class Meta():
	    ordering = ["name"]

    def __str__(self):
        return self.name

class Session(models.Model):
    ticket_price = models.PositiveIntegerField(verbose_name="how much will the ticket cost")
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="current_cinema")
    first_day = models.DateField(default=date.today, verbose_name="First day of the show ")
    last_day = models.DateField(default=date.today, verbose_name="Last day of the show ")
    begins_at = models.TimeField(default=timezone.now, verbose_name="Start ")
    ends_at = models.TimeField(default=timezone.now, verbose_name="End ")
    free_places = models.PositiveIntegerField(blank=True, null=True)

    class Meta():
        ordering = ["ticket_price"]

    def __str__(self):
        return self.cinema.name

class Purchase(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name="purchases")
    date = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Session, on_delete=models.DO_NOTHING, related_name="session")
    ticket_amount = models.PositiveIntegerField(verbose_name="amount of tickets")
    
    class Meta():
	    ordering = ["-date"]

    def save(self, *args, **kwargs):
        ticket_amount = self.ticket_amount
        price = self.ticket.ticket_price
        user = self.user
        ticket = self.ticket
        if user.money >= (price * ticket_amount) and ticket_amount != 0:
            ticket.free_places -= ticket_amount
            user.money -= (price * ticket_amount)
            with transaction.atomic():
                user.save()
                ticket.save()
                super(Purchase, self).save(*args, **kwargs)
        elif ticket.free_places < ticket_amount:
            raise NotEnoughTickets
        elif user.money - (price * ticket_amount) < 0:
            raise NotEnoughMoney
        elif ticket_amount == 0:
            raise CannotBeZero
		
    def __str__(self):
	    return f"{self.ticket.cinema.name}"