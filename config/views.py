#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from hits.models import ResourceView

import stripe


def about(request):

    total_views = ResourceView.objects.total_count()

    average_day = int(round(total_views / ResourceView.objects.count()))

    return render_to_response(
        'pages/about.html',
        {
            'total': total_views,
            'average_day': average_day,
        },
        context_instance=RequestContext(request)
    )


def home(request):

    total_views = ResourceView.objects.total_count()

    total_views = int(round(total_views, -2))

    stripe_key = settings.STRIPE_KEYS['publishable']

    return render_to_response(
        'pages/home.html',
        {
            'total_views': total_views,
            'stripe_key': stripe_key
        },
        context_instance=RequestContext(request)
    )


@csrf_exempt
def stripe_donation(request):
    if request.method == 'POST':
        # Amount in cents
        amount = 1000

        stripe.api_key = settings.STRIPE_KEYS['secret']

        customer = stripe.Customer.create(
            email=request.POST.get('stripeEmail', ''),
            card=request.POST.get('stripeToken', '')
        )

        try:
            stripe.Charge.create(
                customer=customer.id,
                amount=amount,
                currency='usd',
                description='PokeAPI donation'
            )
        except:
            return redirect('/')

        return redirect('/')
    return redirect('/')
