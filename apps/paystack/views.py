import json
import base64
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import RedirectView, TemplateView

# Create your views here.
from . import settings, signals, utils
from .signals import payment_verified
from .utils import load_lib
from django.contrib import messages
from django.dispatch import receiver

from apps.store.models import Payment, Intention

def verify_payment(request, order):
    amount = request.GET.get('amount')
    txrf = request.GET.get('trxref')

    print("Printing Order:", order)
    
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    response = paystack_instance.verify_payment(txrf, amount=int(amount))

    if response[0]:
        payment_verified.send(sender=PaystackAPI, ref=txrf, amount=int(amount) / 100, order=order)

        # 
        obj_instance = Payment.objects.get(ref=order)
        obj_instance.txrf = txrf
        obj_instance.save()
        print("Printing Paystack Reference value:", txrf)
        # 

        return redirect(reverse('paystack:successful_verification', args=[order]), locals())
        
    return redirect(reverse('paystack:failed_verification', args=[order]))


class SuccessView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_SUCCESS_URL == 'paystack:success_page':
            return reverse(settings.PAYSTACK_SUCCESS_URL)
        return settings.PAYSTACK_SUCCESS_URL

class FailedView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_FAILED_URL == 'paystack:failed_page':
            return reverse(settings.PAYSTACK_FAILED_URL)
        return settings.PAYSTACK_FAILED_URL


def success_redirect_view(request, order_id):
    print("Success Redirect View", order_id)
    obj_instance = Payment.objects.get(ref=order_id)
    intention_instance = Intention.objects.get(payment_ref=obj_instance.product.payment_ref)
    url = settings.PAYSTACK_SUCCESS_URL

    if url == 'paystack:success_page':
        url = reverse(url)

    obj_instance.verified =True
    intention_instance.verified = True
    intention_instance.save()
    obj_instance.save()

    return redirect(url+"/"+order_id, permanent=True)


def failure_redirect_view(request, order_id):
    url = settings.PAYSTACK_FAILED_URL
    if url == 'paystack:failed_page':
        url = reverse(url)
    return redirect(url, permanent=True)



def webhook_view(request):
    # ensure that all parameters are in the bytes representation
    digest = utils.generate_digest(request.body)
    signature = request.META['HTTP_X_PAYSTACK_SIGNATURE']
    if digest == signature:
        payload = json.loads(request.body)
        signals.event_signal.send(
            sender=request, event=payload['event'], data=payload['data'])
    return JsonResponse({'status': "Success"})