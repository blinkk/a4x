var DonateController = function($element, $scope) {
  this.dirty = false;
  this.customizing = false;
  this.amount = '';
};


DonateController.prototype.toggleCustomizer = function() {
  this.customizing = !this.customizing;
};


DonateController.prototype.isAmountEqual = function(amount) {
  return !this.dirty || (this.amount == amount);
};


DonateController.prototype.setAmount = function(amount) {
  this.dirty = true;
  this.amount = amount;
};


module.exports = {
  DonateController: DonateController
};
