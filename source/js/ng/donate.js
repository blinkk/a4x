var DonateController = function($element, $scope) {
  this.dirty = false;
  this.amount = '';
};


DonateController.prototype.isAmountEqual = function(amount) {
  return (this.amount == amount) && amount;
};


DonateController.prototype.setAmount = function(amount) {
  this.amount = amount;
  this.dirty = true;
};


module.exports = {
  DonateController: DonateController
};
