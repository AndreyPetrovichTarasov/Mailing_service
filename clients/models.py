from django.db import models


class Client(models.Model):
    objects: models.Manager = models.Manager()
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f'{self.full_name}: {self.email}'
