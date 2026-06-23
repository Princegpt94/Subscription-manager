from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):

    class Meta:

        model = Subscription

        fields = [
            'name',
            'amount',
            'renewal_date',
            'status',
            'is_recurring'
        ]

        widgets = {
            'renewal_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            )
        }