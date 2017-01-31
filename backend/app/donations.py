from . import base
from . import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop



class Donation(base.Model):
    amount = msgprop.MessageProperty(messages.AmountMessage)

    @classmethod
    def create(cls, message):
        ent = cls(amount=message.amount)
        ent.put()
        # TODO: Stripe authorization here
        return ent
