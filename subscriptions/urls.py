from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'add/',
        views.add_subscription,
        name='add_subscription'
    ),

    path(
        'view/',
        views.view_subscriptions,
        name='view_subscriptions'
    ),

    path(
         'edit/<int:id>/',
         views.edit_subscription,
         name='edit_subscription'
    ),

    path(
        'delete/<int:id>/',
        views.delete_subscription,
        name='delete_subscription'
    ),

    path(
         'mark-paid/<int:id>/',
         views.mark_paid,
         name='mark_paid'
    ),

]