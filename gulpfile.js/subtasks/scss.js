const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const sourcemaps = require('gulp-sourcemaps');
const pump = require('pump');

module.exports = function(cb) {
    pump(
        [
            gulp.src('static_src/oscar/scss/*.scss'),
            sourcemaps.init(),
            sass({
                includePaths: [
                    'oscar/static_src/oscar/scss/',
                ],
                outputStyle: null,
            }),
            sourcemaps.write('/'),
            gulp.dest('static_src/oscar/css/')
        ],
        cb
    );
};
