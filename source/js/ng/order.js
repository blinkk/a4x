var rpc = function(method, data) {
  return $.ajax({
      url: '/_api/' + method,
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json'
  });
};


var OrderController = function($element, $scope) {
  this.dirty = false;
  this.customizing = false;
  this.amount = '';
  this.order = {};
  this.skusToQuantities = {};
};


OrderController.prototype.toggleCustomizer = function() {
  this.customizing = !this.customizing;
};


OrderController.prototype.isAmountEqual = function(amount) {
  return !this.dirty || (this.amount == amount);
};


OrderController.prototype.setSkuQuantity = function(sku, quantity, amount) {
  this.dirty = true;
  this.skusToQuantities[sku] = quantity;
  this.amount = amount;
};


OrderController.prototype.setAmount = function(amount) {
  this.dirty = true;
  this.amount = amount;
};


OrderController.prototype.createStripeHandler = function() {
  return StripeCheckout.configure({
    key: 'pk_test_421OpDpSp3zsjIuVHCHZAnrR',
    image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
    locale: 'auto',
    billingAddress: true,
    shippingAddress: true,
    token: function(token) {
      this.createOrder(token);
    }.bind(this)
  });
};


OrderController.prototype.openOrderDialog = function() {
  var numItems = 0;
  for (var sku in this.skusToQuantities) {
    var quantity = this.skusToQuantities[sku];
    numItems += quantity;
  };
  var donation = 0;
  var handler = this.createStripeHandler();
  handler.open({
    name: 'Art for X',
    description: numItems + ' items + $' + donation + ' additional donation',
    amount: 2000
  });
};


OrderController.prototype.createOrder = function(token) {
  var items = [];
  for (var sku in this.skusToQuantities) {
    var quantity = this.skusToQuantities[sku];
    items.push({
      'type': 'sku',
      'parent': sku,
      'quantity': quantity
    });
  }
  var req = {
    'order': {
      'stripe_token': token.id,
      'email': token.email,
      'items': items,
      'shipping': {
          'name': token.card.name,
          'address': {
              'line1': token.card.address_line1,
              'line2': token.card.address_line2,
              'city': token.card.address_city,
              'state': token.card.address_state,
              'country': token.card.country,
              'zip': token.card.address_zip
          },
      }
    }
  };
  rpc('orders.create', req);
};


module.exports = {
  OrderController: OrderController
};
