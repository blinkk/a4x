var classes = require('airkit/utils/classes');
var order = require('./ng/order');
var share = require('./ng/share');
var emailShare = require('./ng/emailshare');
var modal = require('airkit/modal');
var smoothScroll = require('smooth-scroll');
var ui = require('airkit/ui');


var a4x = window.a4x || {};
window.a4x = a4x;


a4x.main = function() {
  initNg();
  initSmoothScroll();
};


function initSmoothScroll() {
  modal.init({
    'history': false
  });
  smoothScroll.init({
    'offset': 30,
    'updateURL': false
  });
}


function initNg() {
  angular.module('a4x', [])
      .controller('OrderController', order.OrderController)
      .controller('ShareController', share.ShareController)
      .controller('EmailShareController', emailShare.EmailShareController)
      .config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
      }])
      .run(function($rootScope) {
        // Hide the header donate button when the 'pay' button is visible.
        var update = function() {
          var donateHeader = document.getElementById('donate-header');
          var donateSentinel = document.getElementById('donate-sentinel');
          if (!donateHeader || !donateSentinel) {
            return;
          }
          var enabled = ui.isElementInView(donateSentinel, undefined, true);
          classes.enable(donateHeader, 'header__aside__content--hidden', enabled);
        };
        window.addEventListener('resize', update);
        window.addEventListener('scroll', update);
        window.setTimeout(update, 10);
      })
      .filter('dayDiff', function() {
        return function(otherString) {
          if (!otherString) {
            return '';
          }
          var now = new Date();
          var other = new Date(otherString);
          return Math.trunc((other - now)/(1000 * 60 * 60 * 24));
        }
      })
      .filter('int', function() {
	return function(input) {
          return input ? parseInt(input) : '';
	}
      });
  angular.bootstrap(document, ['a4x']);
}
