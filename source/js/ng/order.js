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
  this.customizing = true;
  this.amount = '';
  this.order = {};
  this.campaignIdent = null;
  this.skusToItems = {};
  this.quantities = {};
  this.quantityOptions = [];
  this.additionalAmount = null;
  for (var i = 0; i < 50; i++) {
    this.quantityOptions.push(i);
  }
};


OrderController.prototype.getTotal = function() {
  var total = 0;
  for (var sku in this.quantities) {
    total += this.skusToItems[sku]['price'] * this.quantities[sku];
  }
  if (this.additionalAmount) {
    total += parseInt(this.additionalAmount);
  }
  return total;
};


OrderController.prototype.setDefaults = function(ident, options) {
  this.setCampaignIdent(ident);
  options.forEach(function(option) {
    this.skusToItems[option['stripe_sku']] = option;
    this.quantities[option['stripe_sku']] = option['default_amount'].toString();
  }.bind(this));
};


OrderController.prototype.setCampaignIdent = function(ident) {
  this.campaignIdent = ident;
  this.getCampaign(ident);
};


OrderController.prototype.getCampaign = function(ident) {
  var req = {
    'campaign': {
      'ident': ident
    }
  };
  rpc('campaigns.get', req).success(function(resp) {
    console.log(resp);
  });
};


OrderController.prototype.toggleCustomizer = function() {
  this.customizing = !this.customizing;
};


OrderController.prototype.isAmountEqual = function(amount) {
  return !this.dirty || (this.amount == amount);
};


OrderController.prototype.setSkuItem = function(sku, item, amount) {
  console.log('test');
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


OrderController.prototype.openOrderDialog = function() {
  var numItems = 0;
  for (var sku in this.quantities) {
    var quantity = this.quantities[sku];
    numItems += quantity;
  };
  numItems = parseInt(numItems);
  var handler = this.createStripeHandler();
  var noun = numItems == 1 ? 'item' : 'items';
  var amount = this.getTotal() * 100;
  var donation = this.additionalAmount || 0;
  handler.open({
    name: 'Art for X',
    description: numItems + ' ' + noun + ', $' + donation + ' on top',
    amount: amount 
  });
};


OrderController.prototype.createOrder = function(token) {
  var total = this.getTotal() * 100;
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
