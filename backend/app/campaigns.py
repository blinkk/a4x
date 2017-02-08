from . import base
from . import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop



class Campaign(base.Model):
    end = ndb.DateTimeProperty()
    goal = ndb.FloatProperty()
    num_orders = ndb.IntegerProperty()
    raised = ndb.FloatProperty()
    start = ndb.DateTimeProperty()

    @classmethod
    def get(cls, ident):
        key = ndb.Key('Campaign', ident)
        return key.get()

    @classmethod
    def get_or_create(cls, ident):
        key = ndb.Key('Campaign', ident)
        ent = key.get()
        if ent is None:
            ent = cls(key=key)
            ent.put()
        return ent

    @property
    def percent_raised(self):
        if self.raised and self.goal:
            return self.raised / self.goal * 100
        return 0.0

    def add_order(self, order):
        self.num_orders = self.num_orders or 0
        self.num_orders += 1
        self.raised += order.amount
        self.put()

    def to_message(self):
        msg = messages.CampaignMessage()
        msg.num_orders = self.num_orders
        msg.raised = self.raised
        msg.goal = self.goal
        msg.ident = self.ident
        msg.percent_raised = self.percent_raised
        msg.end = self.end
        msg.start = self.start
        return msg
