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
  this.campaignIdent = null;
  this.skusToItems = {};
};


OrderController.prototype.toggleCustomizer = function() {
  this.customizing = !this.customizing;
};


OrderController.prototype.isAmountEqual = function(amount) {
  return !this.dirty || (this.amount == amount);
};


OrderController.prototype.setSkuItem = function(sku, item, amount) {
  this.dirty = true;
  this.skusToItems[sku] = item;
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


OrderController.prototype.getAmount = function() {
  var total = 0;
  for (var sku in this.skusToItems) {
    var item = this.skusToItems[sku];
    total += item['quantity'] * item['price'];
  }
  return total;
};


OrderController.prototype.openOrderDialog = function() {
  var numItems = 0;
  for (var sku in this.skusToItems) {
    var quantity = this.skusToItems[sku]['quantity'];
    numItems += quantity;
  };
  var donation = 0;
  numItems = parseInt(numItems);
  var handler = this.createStripeHandler();
  var noun = numItems == 1 ? 'item' : 'items';
  var amount = this.getAmount() * 100;
  handler.open({
    name: 'Art for X',
    description: numItems + ' ' + noun + ', $' + donation + ' on top',
    amount: amount 
  });
};


OrderController.prototype.createOrder = function(token) {
  var amount = this.getAmount() * 100;
  var items = [];
  for (var sku in this.skusToItems) {
    var quantity = this.skusToItems[sku]['quantity'];
    items.push({
      'type': 'sku',
      'parent': sku,
      'quantity': quantity
    });
  }
  var req = {
    'order': {
      'campaign_ident': this.campaignIdent,
      'stripe_token': token.id,
      'amount': amount,
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
