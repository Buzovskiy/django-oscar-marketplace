'use strict';
// Сборщики статики oscar
const oscar = require('./oscar');
// Сборщики установленного шаблона
const custom = require('./custom');

/* подключаем gulp и плагины */
var gulp = require('gulp'),  // подключаем Gulp
    plumber = require('gulp-plumber'), // модуль для отслеживания ошибок
    rigger = require('gulp-rigger'), // модуль для импорта содержимого одного файла в другой
    sourcemaps = require('gulp-sourcemaps'), // модуль для генерации карты исходных файлов
    sass = require('gulp-sass'), // модуль для компиляции SASS (SCSS) в CSS
    autoprefixer = require('gulp-autoprefixer'), // модуль для автоматической установки автопрефиксов
    cleanCSS = require('gulp-clean-css'), // плагин для минимизации CSS
    uglify = require('gulp-uglify'), // модуль для минимизации JavaScript
    cache = require('gulp-cache'), // модуль для кэширования
    imagemin = require('gulp-imagemin'), // плагин для сжатия PNG, JPEG, GIF и SVG изображений
    jpegrecompress = require('imagemin-jpeg-recompress'), // плагин для сжатия jpeg	
    pngquant = require('imagemin-pngquant'), // плагин для сжатия png
    del = require('del'), // плагин для удаления файлов и каталогов
    rename = require('gulp-rename');


//     var path_to_build = 'static_src/custom/build';
//     var path_to_src = 'static_src/custom/src'; 
    
// /* пути к исходным файлам (src), к готовым файлам (build), а также к тем, за изменениями которых нужно наблюдать (watch) */
// var path = {
//     build: {
//         js: `${path_to_build}/js/`,
//         css: `${path_to_build}/css/`,
//         img: `${path_to_build}/img/`,
//     },
//     src: {
//         js: `${path_to_src}/js/main.js`,
//         style: `${path_to_src}/style/main.scss`,
//         img: `${path_to_src}/img/**/*.*`,
//     },
//     watch: {
//         js: `${path_to_src}/js/**/*.js`,
//         css: `${path_to_src}/style/**/*.scss`,
//         img: `${path_to_src}/img/**/*.*`,
//     },
//     clean: `./${path_to_build}/*`
// };

// /* задачи */

// сбор стилей
gulp.task('css:build', custom.cssBuild);

// сбор js
gulp.task('js:build', custom.jsBuild);

// очистка кэша
gulp.task('cache:clear', function () {
    cache.clearAll();
});

// обработка картинок
gulp.task('image:clean', function(){
    return del(`${custom.path.clean_img}`);
});
gulp.task('image:build:only', custom.imageBuild);
gulp.task('image:build', gulp.series('image:clean', 'image:build:only'));

// удаление каталога build 
gulp.task('clean:build', function () {
    return del(custom.path.clean);
});

// сборка
gulp.task('build',
    gulp.series(
        'clean:build',
        gulp.parallel(
            'css:build',
            'js:build',
            'image:build'
        )
    )
);

gulp.task('oscar:css:build', oscar.cssBuild);

// запуск задач при изменении файлов
gulp.task('watch', function () {
    gulp.watch(custom.path.watch.css, gulp.series('css:build'));
    gulp.watch(custom.path.watch.js, gulp.series('js:build'));
    gulp.watch(custom.path.watch.img, gulp.series('image:build'));
    gulp.watch(oscar.path.watch.css, gulp.series('oscar:css:build'));
});

// запуск задач при изменении файлов
gulp.task('watch:css', function(){
    gulp.watch(custom.path.watch.css, gulp.series('css:build'));
});

// запуск задач при изменении файлов
gulp.task('watch:js', function(){
    gulp.watch(custom.path.watch.js, gulp.series('js:build'));
});

// задача по умолчанию
gulp.task('default', gulp.series(
//     'build',
    'watch'
));