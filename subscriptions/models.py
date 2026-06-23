from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):

    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Due', 'Due'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    renewal_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Due'
    )

    is_recurring = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name