var order = require('./ng/order');


var a4x = window.a4x || {};
window.a4x = a4x;


a4x.main = function() {
  initNg();
};


function initNg() {
  angular.module('a4x', [])
      .controller('OrderController', order.OrderController)
      .config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
      }]);
  angular.bootstrap(document, ['a4x']);
}
