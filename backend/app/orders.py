from . import base
from . import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

import stripe

DESCRIPTION = 'Art for X Invoice'


class Order(base.Model):
    amount = ndb.FloatProperty()
    num_items = ndb.IntegerProperty()
    note = ndb.StringProperty()

    @classmethod
    def create_stripe_order(cls, message):
        try:
            stripe_items = [{
                'type': 'sku',
                'quantity': item.quantity,
                'parent': item.parent,
            } for item in message.items]
            stripe_order = stripe.Order.create(
              currency='usd',
              items=stripe_items,
              email=message.email,
              shipping={
                'name': message.shipping.name,
                'address':{
                    'line1': message.shipping.address.line1,
                    'city': message.shipping.address.city,
                    'country': message.shipping.address.country,
                    'postal_code': message.shipping.address.postal_code,
                },
              },
            )
            return stripe_order
        except stripe.CardError:
            self.response.status_int = 400
            self.response.out.write('Error processing payment.')
        num_items = 0
        for item in message.items:
            num_items += item.quantity
        ent = cls(amount=message.amount, num_items=num_items)
        ent.put()
        return ent

    @classmethod
    def create_test(cls):
        order_message = cls.create_test_message()
        cls.create_stripe_order(order_message)

    @classmethod
    def create_test_message(cls):
        address_message = messages.AddressMessage(
                line1='1234 1st St',
                city='San Francisco',
                country='US',
                postal_code='94110')
        items_message = [
                messages.ItemMessage(parent='sku_A2kY1fnyd8ecUt', type='sku'),
                messages.ItemMessage(parent='sku_A2kYvzKCTUaR2N', type='sku')]
        shipping_message = messages.ShippingMessage(
                name='Breakfast at Tiffany\'s',
                address=address_message)
        order_message = messages.OrderMessage(
                email='user@example.com',
                shipping=shipping_message,
                items=items_message)
        return order_message
