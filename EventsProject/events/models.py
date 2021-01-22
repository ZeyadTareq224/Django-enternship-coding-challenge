from django.db import models
import django

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover_img = models.ImageField()
    date = models.DateField(default= django.utils.timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_participants_count(self):
        participants_count = self.eventsubscribtion_set.count()
        return participants_count

    def save(self, *args, **kwargs):
        if self.date < timezone.now().date():
            raise ValidationError("The date cannot be in the past!")
        super(Event, self).save(*args, **kwargs)






class EventSubscribtion(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.username} Subscriptions"

    