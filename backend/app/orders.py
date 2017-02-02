from . import base
from . import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

import stripe

DESCRIPTION = 'Art for X Invoice'


class Order(base.Model):

    @classmethod
    def create_stripe_order(cls, message):
        try:
            stripe_items = [{
                'type': 'sku',
                'parent': item.stripe_id
            } for item in message.items]
            stripe.Order.create(
              currency='usd',
              items=stripe_items,
              shipping={
                "name": message.shipping.name,
                "address":{
                  "line1": message.shipping.address.line1,
                  "city": message.shipping.address.city,
                  "country": message.shipping.address.country,
                  "postal_code": message.shipping.address.postal_code,
                },
              },
              email=message.email,
            )
        except stripe.CardError:
            self.response.status_int = 400
            self.response.out.write('Error processing payment.')
            return

    @classmethod
    def create_test(cls):
        address_message = messages.AddressMessage(
                line1='1234 1st St',
                city='San Francisco',
                country='US',
                postal_code='94110')
        items_message = [
                messages.ItemMessage(stripe_id='sku_A2kY1fnyd8ecUt'),
                messages.ItemMessage(stripe_id='sku_A2kYvzKCTUaR2N')]
        shipping_message = messages.ShippingMessage(
                name='Breakfast at Tiffany\'s',
                address=address_message)
        order_message = messages.OrderMessage(
                email='user@example.com',
                shipping=shipping_message,
                items=items_message)
        cls.create_stripe_order(order_message)
