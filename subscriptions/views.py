from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Subscription
from .forms import SubscriptionForm
from .user_forms import RegisterForm

from dateutil.relativedelta import relativedelta


def home(request):

    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    return render(request, 'index.html')


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account created successfully! Please login."
            )

            return redirect('/accounts/login/')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


@login_required
def dashboard(request):

    subscriptions = Subscription.objects.filter(
        user=request.user
    )

    paid_count = subscriptions.filter(
        status='Paid'
    ).count()

    due_count = subscriptions.filter(
        status='Due'
    ).count()

    unpaid_count = subscriptions.filter(
        status='Unpaid'
    ).count()

    total_amount = sum(
        sub.amount for sub in subscriptions
    )

    context = {
        'subscriptions': subscriptions,
        'paid_count': paid_count,
        'due_count': due_count,
        'unpaid_count': unpaid_count,
        'total_amount': total_amount,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


@login_required
def add_subscription(request):

    if request.method == 'POST':

        form = SubscriptionForm(request.POST)

        if form.is_valid():

            subscription = form.save(commit=False)

            subscription.user = request.user

            subscription.save()

            messages.success(
                request,
                "Subscription added successfully!"
            )

            return redirect('dashboard')

    else:

        form = SubscriptionForm()

    return render(
        request,
        'add_subscription.html',
        {'form': form}
    )


@login_required
def view_subscriptions(request):

    subscriptions = Subscription.objects.filter(
        user=request.user
    )

    return render(
        request,
        'view_subscription.html',
        {
            'subscriptions': subscriptions
        }
    )


@login_required
def delete_subscription(request, id):

    subscription = get_object_or_404(
        Subscription,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        subscription.delete()

        messages.success(
            request,
            "Subscription deleted successfully!"
        )

        return redirect('view_subscriptions')

    return render(
        request,
        'delete_subscription.html',
        {
            'subscription': subscription
        }
    )


@login_required
def edit_subscription(request, id):

    subscription = get_object_or_404(
        Subscription,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = SubscriptionForm(
            request.POST,
            instance=subscription
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Subscription updated successfully!"
            )

            return redirect('view_subscriptions')

    else:

        form = SubscriptionForm(
            instance=subscription
        )

    return render(
        request,
        'edit_subscription.html',
        {
            'form': form
        }
    )


@login_required
def mark_paid(request, id):

    subscription = get_object_or_404(
        Subscription,
        id=id,
        user=request.user
    )

    if subscription.is_recurring:

        # Move renewal date to next month
        subscription.renewal_date += relativedelta(months=1)

        # Next month's payment becomes Due
        subscription.status = 'Due'

    else:

        # One-time subscription remains Paid
        subscription.status = 'Paid'

    subscription.save()

    messages.success(
        request,
        "Payment recorded successfully!"
    )

    return redirect('view_subscriptions')