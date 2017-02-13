from protorpc import messages
from protorpc import message_types


class ItemMessage(messages.Message):
    parent = messages.StringField(1)
    quantity = messages.IntegerField(2, default=1)
    type = messages.StringField(3)


class AddressMessage(messages.Message):
    line1 = messages.StringField(1)
    line2 = messages.StringField(2)
    city = messages.StringField(3)
    country = messages.StringField(4)
    postal_code = messages.StringField(5)


class ShippingMessage(messages.Message):
    name = messages.StringField(1)
    address = messages.MessageField(AddressMessage, 2)


class OrderMessage(messages.Message):
    email = messages.StringField(1)
    shipping = messages.MessageField(ShippingMessage, 2)
    items = messages.MessageField(ItemMessage, 3, repeated=True)
    stripe_token = messages.StringField(4)
    amount = messages.FloatField(5)
    artist_note = messages.StringField(6)
    campaign_ident = messages.StringField(7)
    artist_tip = messages.FloatField(8)
    extra_donation = messages.FloatField(9)


class CampaignMessage(messages.Message):
    num_orders = messages.IntegerField(1)
    raised = messages.FloatField(2)
    goal = messages.FloatField(3)
    percent_raised = messages.FloatField(4)
    start = message_types.DateTimeField(5)
    end = message_types.DateTimeField(6)
    ident = messages.StringField(7)
    average = messages.FloatField(8)


class OrderRequest(messages.Message):
    order = messages.MessageField(OrderMessage, 1)


class OrderResponse(messages.Message):
    order = messages.MessageField(OrderMessage, 1)
    campaign = messages.MessageField(CampaignMessage, 2)


class CampaignRequest(messages.Message):
    campaign = messages.MessageField(CampaignMessage, 1)


class CampaignResponse(messages.Message):
    campaign = messages.MessageField(CampaignMessage, 1)
