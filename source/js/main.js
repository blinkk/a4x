var modal = require('airkit/modal');
var DonateController = require('./ng/donate');

var a4x = window.a4x || {};
window.a4x = a4x;

a4x.main = function() {
  modal.init();
  initNg();
};


function initNg() {
  angular.module('a4x', [])
      .controller('DonateController', DonateController)
      .config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
      }]);
  angular.bootstrap(document, ['a4x']);
}
