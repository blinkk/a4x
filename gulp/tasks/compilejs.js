var airkit = require('airkit/gulp/compilejs');
var config = require('../config');

module.exports = function() {
  return airkit.compilejs(
      config.JS_SOURCES, config.JS_OUT_DIR, config.JS_OUT_FILE,
      config.JS_OPTIONS);
};
