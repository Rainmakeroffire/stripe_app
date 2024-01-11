from django.urls import path
from .views import (create_checkout_session, create_order_checkout_session, create_payment_intent,
                    item_detail, order_detail, intent, success, cancel, menu)

urlpatterns = [
    path('buy/<int:item_id>/', create_checkout_session, name='get_session_id'),
    path('buy_order/<int:order_id>/', create_order_checkout_session, name='get_order_session_id'),
    path('pay/<int:order_id>/', create_payment_intent, name='create_payment_intent'),

    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('intent/<int:order_id>/', intent, name='intent'),

    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('', menu, name='menu'),
]

