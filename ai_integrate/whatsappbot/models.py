from django.db import models

# Create your models here.

class Property(models.Model):
    broker_name = models.CharField(max_length=120)
    description = models.TextField()
    images = models.JSONField(default=list, blank=True)
    ai_structure = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.broker_name} | {self.description[:40]}"
