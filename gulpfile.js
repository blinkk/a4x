var gulp = require('./gulp')([
  'compilejs',
  'watchjs'
]);

gulp.task('build', ['compilejs']);
gulp.task('default', ['watchjs']);
