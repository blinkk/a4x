from . import base
from . import emails
from . import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop



class Campaign(base.Model):
    end = ndb.DateTimeProperty()
    goal = ndb.FloatProperty(default=1000)
    num_orders = ndb.IntegerProperty()
    raised = ndb.FloatProperty()
    start = ndb.DateTimeProperty()
    artist_name = ndb.StringProperty()
    title = ndb.StringProperty()
    story = ndb.TextProperty()

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
            val = self.raised / self.goal * 100
            val = '{0:.2f}'.format(round(val, 2))
            return float(val)
        return 0.0

    @property
    def url(self):
        return 'https://artforx.com/'

    @property
    def average(self):
        if self.raised and self.goal:
            val = self.raised / self.num_orders
            val = '{0:.2f}'.format(round(val, 2))
            return float(val)
        return 0.0

    def add_order(self, order):
        self.num_orders = self.num_orders or 0
        self.num_orders += 1
        self.raised = self.raised or 0
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
        msg.average = self.average
        return msg

    def send_email(self, message):
        emailer = emails.Emailer(sender_name=message.sender_name)
        subject = 'I just donated to the ACLU by supporting an art fundraising campaign'
        kwargs = {
            'campaign': self,
            'user_supplied_body': message.user_supplied_body,
        }
        emailer.send(
            to=[message.recipient_email, message.sender_email],
            subject=subject,
            template='email.html',
            kwargs=kwargs)
