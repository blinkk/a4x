from . import messages
from . import orders


class OrderService(remote.Service):

    @remote.method(messages.OrderRequest
                   messages.OrderResponse)
    def create(self, request):
        order = orders.Order.create_stripe_order(request.order)
        resp = messages.OrderResponse()
#        resp.order = order.to_message()
        return resp
