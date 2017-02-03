from protorpc import messages


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


class CampaignMessage(messages.Message):
    num_orders = messages.IntegerField(1)
    raised = messages.FloatField(2)
    goal = messages.FloatField(3)


class OrderRequest(messages.Message):
    order = messages.MessageField(OrderMessage, 1)


class OrderResponse(messages.Message):
    order = messages.MessageField(OrderMessage, 1)
