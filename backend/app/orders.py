from . import base
from . import campaigns
from . import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

import stripe

DESCRIPTION = 'Art for X Invoice'


class Order(base.Model):
    amount = ndb.FloatProperty()
    num_items = ndb.IntegerProperty()
    campaign_ident = ndb.StringProperty()
    artist_note = ndb.StringProperty()
    artist_tip = ndb.FloatProperty()

    @property
    def campaign(self):
        return campaigns.Campaign.get(self.campaign_ident)

    @classmethod
    def create_stripe_order(cls, message):
        try:
            metadata = {
                'artist_tip': message.artist_tip,
                'artist_note': message.artist_note,
                'extra_donation': message.extra_donation,
            }
            stripe_items = [{
                'type': 'sku',
                'quantity': item.quantity,
                'parent': item.parent,
            } for item in message.items if item.quantity]
            stripe_order = stripe.Order.create(
                metadata=metadata,
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
            charge = stripe.Charge.create(
                receipt_email=message.email,
                metadata=metadata,
                amount=int(message.amount * 100),
                currency='usd',
                description=message.stripe_title,
                source=message.stripe_token,
            )
        except stripe.CardError:
            self.response.status_int = 400
            self.response.out.write('Error processing payment.')
        num_items = 0
        for item in message.items:
            num_items += item.quantity

        ent = cls(
            amount=message.amount,
            artist_tip=message.artist_tip,
            artist_note=message.artist_note,
            num_items=num_items,
            campaign_ident=message.campaign_ident)
        ent.put()
        campaign = campaigns.Campaign.get_or_create(message.campaign_ident)
        campaign.add_order(ent)
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

    def to_message(self):
        msg = messages.OrderMessage()
        return msg
