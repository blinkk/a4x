module.exports = {
  JS_SOURCES: [
    './source/js/main.js'
  ],
  JS_OPTIONS: {
    uglify: {
      mangle: false
    }
  },
  JS_OUT_DIR: './dist/js/',
  JS_OUT_FILE: 'main.min.js'
};
