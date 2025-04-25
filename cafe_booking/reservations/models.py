from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils import timezone   
from django.utils.timezone import now, localtime, is_aware, make_aware


class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    
class Cafe(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    table_count = models.PositiveIntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    motto = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date', 'time')  # prevent double booking by same user

    def is_past(self):
        dt = timezone.datetime.combine(self.date, self.time)

        # Make sure dt is awar
        if not is_aware(dt):
            dt = make_aware(dt)

        return dt < localtime(now())  # Compare using local time


    def __str__(self):
        return f"{self.user.username} → {self.cafe.name} on {self.date} at {self.time}"
