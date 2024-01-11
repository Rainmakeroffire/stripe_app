from django.shortcuts import render
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order
from stripe_app.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY, DOMAIN_NAME


@csrf_exempt
def create_checkout_session(request, item_id):
    stripe.api_key = STRIPE_SECRET_KEY
    item = Item.objects.get(pk=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=DOMAIN_NAME + 'success/',
        cancel_url=DOMAIN_NAME + 'cancel/',
    )
    return JsonResponse({'session_id': session.id})


@csrf_exempt
def create_order_checkout_session(request, order_id):
    stripe.api_key = STRIPE_SECRET_KEY
    order = Order.objects.get(pk=order_id)

    coupon = stripe.Coupon.create(
        percent_off=int(order.discount.ratio * 100),
        duration='once',
    )
    coupon_id = coupon.id

    tax_rate = stripe.TaxRate.create(
        display_name="VAT",
        inclusive=False,
        percentage=float(order.tax.rate * 100),
    )
    tax_rate_id = tax_rate.id

    line_items = [
        {
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
            'tax_rates': [tax_rate_id],
        }
        for item in order.items.all()
    ]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        discounts=[{
            'coupon': coupon_id,
        }],
        mode='payment',
        success_url=DOMAIN_NAME + 'success/',
        cancel_url=DOMAIN_NAME + 'cancel/',
    )

    return JsonResponse({'session_id': session.id})


def create_payment_intent(request, order_id):
    stripe.api_key = STRIPE_SECRET_KEY
    order = Order.objects.get(pk=order_id)

    order.calculate_total_amount()

    intent = stripe.PaymentIntent.create(
        amount=int(order.total_amount * 100),
        currency=order.currency,
    )

    return JsonResponse({'clientSecret': intent.client_secret})


def item_detail(request, item_id):
    item = Item.objects.get(pk=item_id)
    return render(request, 'item_detail.html', {'item': item, 'stripe_public_key': STRIPE_PUBLIC_KEY})


def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'order_detail.html', {'order': order, 'stripe_public_key': STRIPE_PUBLIC_KEY})


def intent(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.calculate_total_amount()
    return render(request, 'intent.html', {'order': order, 'stripe_public_key': STRIPE_PUBLIC_KEY})


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
