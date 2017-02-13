module.exports = {
  JS_SOURCES: [
    './node_modules/smooth-scroll/dist/js/smooth-scroll.js',
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
