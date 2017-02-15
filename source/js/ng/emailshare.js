var rpc = function(method, data) {
  return $.ajax({
      url: '/_api/' + method,
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json'
  });
};


var EmailShareController = function($element, $scope) {
  this.$scope = $scope;
  this.campaignIdent = null;
  this.el = $element[0];
  this.isLoading = false;
  var textareaEl = this.el.querySelector('textarea');
  // $(textareaEl).height($(textareaEl)[0].scrollHeight);
  // console.log(textareaEl);
  this.email = {
    sender_email: '',
    recipient_email: '',
    user_supplied_body: 'Dear friend,\n\nI just donated to the ACLU by backing a fundraising campaign on Art for X. Here\'s a digital postcard for you containing the art. Check it out below!'
  };
};


EmailShareController.prototype.submit = function() {
  var req = {
    'campaign': {
      'ident': this.campaignIdent
    },
    'email': this.email
  };
  this.isLoading = true;
  rpc('campaigns.send_email', req).success(function(resp) {
    // Add a one second delay to avoid misclicks.
    window.setTimeout(function() {
      this.isLoading = false;
      this.isSubmitted = true;
      this.$scope.$apply();
    }.bind(this), 1000);
  }.bind(this)).failure(function() {
    alert('Sorry, there was a problem sending your email.');
    this.isLoading = false;
    this.$scope.$apply();
  });
};


module.exports = {
  EmailShareController: EmailShareController
};
