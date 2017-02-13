var ShareController = function($scope) {
};


ShareController.prototype.openFacebook = function() {
  var url = 'https://' + window.location.host;
  FB.ui({
    method: 'feed',
    link: url
  });
};


ShareController.prototype.openTwitter = function(text) {
  var url = 'https://twitter.com/share?text=' + text;
  window.open(url, '',
      'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,' +
      'height=300,width=600,top=100,left=100');
};


module.exports = {
  ShareController: ShareController
};
