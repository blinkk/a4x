from . import campaigns
from . import messages
from . import orders
from protorpc import remote


class CampaignService(remote.Service):

    @remote.method(messages.CampaignRequest,
                   messages.CampaignResponse)
    def get(self, request):
        campaign = campaigns.Campaign.get_or_create(request.campaign.ident)
        resp = messages.CampaignResponse()
        resp.campaign = campaign.to_message()
        return resp


class OrderService(remote.Service):

    @remote.method(messages.OrderRequest,
                   messages.OrderResponse)
    def create(self, request):
        order = orders.Order.create_stripe_order(request.order)
        resp = messages.OrderResponse()
#        resp.order = order.to_message()
        return resp
