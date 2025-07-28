
from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"
