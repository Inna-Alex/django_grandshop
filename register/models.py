from django.db import models
from django.contrib.auth.models import User
import uuid

"""class CustomerUser(User):

    Model representing customer

    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID")
    phone = models.SlugField(max_length=11)

    def get_absolute_url(self):
        return reverse('customer_detail', args=[str(self.customer_id)])

    def __str__(self):
        return self.login

    class Meta:
        ordering = ['username']"""
