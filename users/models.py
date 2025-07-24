from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True)
    is_google = models.BooleanField(default=False)

    def __str__(self):
        return self.email
