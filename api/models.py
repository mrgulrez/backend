
from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"

class Build(models.Model):
    build_id = models.CharField(max_length=50, unique=True)
    frame = models.CharField(max_length=100)
    propellers = models.CharField(max_length=100, blank=True, null=True)
    motors = models.CharField(max_length=100, blank=True, null=True)
    battery = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.build_id