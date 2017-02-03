from . import orders
from . import messages
from . import testing


class OrdersTestCase(testing.TestCase):

    def test_create(self):
        order_message = orders.Order.create_test_message()
        orders.Order.create_stripe_order(order_message)


if __name__ == '__main__':
    unittest.main()
