var gulp = require('gulp');
var sass = require('gulp-sass');
var browserSync = require('browser-sync').create();
var runSequence = require('run-sequence');

gulp.task('sass', function () {
  return gulp.src('catflapsite/static/sass/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('catflapsite/static/css'));
});

gulp.task('browserSync', function() {
    browserSync.init(
      ["catflapsite/static/css/*.css", "catflapsite/static/javascript/*.js", 'templates/*.html'], {
        proxy:  "localhost:8000"
    });
});

gulp.task('watch', function() {
  gulp.watch('catflapsite/static/sass/*.scss', ['sass']);
});


gulp.task('default', function() {
    runSequence('sass', 'browserSync', 'watch');
});