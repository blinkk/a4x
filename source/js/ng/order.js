var smoothScroll = require('smooth-scroll');


var rpc = function(method, data) {
  return $.ajax({
      url: '/_api/' + method,
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json'
  });
};


var OrderController = function($element, $scope) {
  this.$scope = $scope;
  this.dirty = false;
  this.customizing = true;
  this.amount = '';
  this.order = {};
  this.campaignIdent = null;
  this.campaign = null;
  this.skusToItems = {};
  this.quantities = {};
  this.quantityOptions = [];
  this.additionalAmount = null;
  this.artistTip = null;
  this.artistNote = null;
  this.stripeImageUrl = null;
  this.stripeCheckoutKey = null;
  this.isSubmitted = false;
  this.isOptionalShown = false;
  this.stripeTitle = false;
  for (var i = 0; i < 50; i++) {
    this.quantityOptions.push(i);
  }
};


OrderController.prototype.getAddMoreAmount = function() {
  if (this.campaign) {
    return this.campaign.average - this.getTotalMinusTip();
  }
};


OrderController.prototype.getTotalMinusTip = function() {
  if (this.artistTip) {
    return this.getTotal() - this.artistTip;
  }
  return this.getTotal();
};


OrderController.prototype.getTotal = function() {
  var total = 0;
  for (var sku in this.quantities) {
    total += this.skusToItems[sku]['price'] * this.quantities[sku];
  }
  if (this.additionalAmount) {
    total += parseInt(this.additionalAmount);
  }
  if (this.artistTip) {
    total += parseInt(this.artistTip);
  }
  return total;
};


OrderController.prototype.setDefaults =
    function(ident, options, stripeImageUrl, stripeCheckoutKey, stripeTitle) {
  this.stripeImageUrl = stripeImageUrl;
  this.stripeCheckoutKey = stripeCheckoutKey;
  this.stripeTitle = stripeTitle;
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
    this.campaign = resp['campaign'];
    this.$scope.$apply();
  }.bind(this));
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


OrderController.prototype.createStripeHandler = function() {
  return StripeCheckout.configure({
    key: this.stripeCheckoutKey,
    image: this.stripeImageUrl,
    locale: 'auto',
    billingAddress: true,
    shippingAddress: true,
    token: function(token) {
      this.createOrder(token);
    }.bind(this)
  });
};


OrderController.prototype.goNext = function() {
  this.isOptionalShown = true;
  window.setTimeout(function() {
    smoothScroll.animateScroll('#order-note');
  }, 10);
};


OrderController.prototype.openOrderDialog = function() {
  var numItems = 0;
  for (var sku in this.quantities) {
    var quantity = this.quantities[sku];
    numItems += parseInt(quantity);
  };
  numItems = parseInt(numItems);
  var handler = this.createStripeHandler();
  var noun = numItems == 1 ? 'item' : 'items';
  var amount = this.getTotal() * 100;
  var donation = this.additionalAmount || 0;
  var tip = this.artistTip || 0;
  var description = numItems + ' ' + noun + ', $' + donation +
      ' extra donation, $' + tip + ' tip';
  handler.open({
    name: this.stripeTitle,
    description: description,
    amount: amount 
  });
};


OrderController.prototype.createOrder = function(token) {
  var total = this.getTotal();
  var items = [];
  for (var sku in this.skusToItems) {
    var quantity = this.quantities[sku];
    items.push({
      'type': 'sku',
      'parent': sku,
      'quantity': quantity
    });
  }
  var req = {
    'order': {
      'campaign_ident': this.campaignIdent,
      'artist_tip': this.artistTip,
      'artist_note': this.artistNote,
      'stripe_token': token.id,
      'amount': total,
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
  rpc('orders.create', req).success(function(resp) {
    this.campaign = resp['campaign'];
    this.isSubmitted = true;
    this.isOptionalShown = false;
    this.$scope.$apply();
  }.bind(this));
};


module.exports = {
  OrderController: OrderController
};
