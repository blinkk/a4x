from . import orders
from . import messages
from . import testing


class OrdersTestCase(testing.TestCase):

    def test_create(self):
        address_message = messages.AddressMessage(
                line1='1234 1st St',
                city='San Francisco',
                country='US',
                postal_code='94110')
        items_message = [
                messages.ItemMessage(stripe_id='prod_A2jhaQUXxL4J4Q'),
                messages.ItemMessage(stripe_id='prod_A2jhuznELLtveg')]
        shipping_message = messages.ShippingMessage(
                name='Breakfast at Tiffany\'s',
                address=address_message)
        order_message = messages.OrderMessage(
                email='user@example.com',
                shipping=shipping_message,
                items=items_message)
        orders.Order.create_stripe_order(order_message)


if __name__ == '__main__':
    unittest.main()
