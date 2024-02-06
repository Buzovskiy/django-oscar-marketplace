'use strict';
// Сборщики статики oscar
const oscar = require('./oscar');
// Сборщики установленного шаблона
const custom = require('./custom');

/* подключаем gulp и плагины */
var gulp = require('gulp'),  // подключаем Gulp
    cache = require('gulp-cache'), // модуль для кэширования
    del = require('del'); // плагин для удаления файлов и каталогов

/* задачи */

// сбор стилей
gulp.task('css:build:only', custom.cssBuild);
gulp.task('css:build:copyWebfonts', custom.copyWebfonts);

gulp.task('css:build', gulp.series('css:build:only', 'css:build:copyWebfonts'));

// сбор js библиотек
gulp.task('js:libs:build', custom.jsLibsBuild);

// сбор js приложения
gulp.task('js:app:build', custom.jsAppBuild);

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
            'js:libs:build',
            'js:app:build',
            'image:build',
        )
    )
);

gulp.task('oscar:css:build', oscar.cssBuild);

// запуск задач при изменении файлов
gulp.task('watch', function () {
    gulp.watch(custom.path.watch.css, gulp.series('css:build'));
    gulp.watch(custom.path.watch.js.libs, gulp.series('js:libs:build'));
    gulp.watch(custom.path.watch.js.app, gulp.series('js:app:build'));
    gulp.watch(custom.path.watch.img, gulp.series('image:build'));
    gulp.watch(oscar.path.watch.css, gulp.series('oscar:css:build'));
});

// запуск задач при изменении файлов
gulp.task('watch:css', function(){
    gulp.watch(custom.path.watch.css, gulp.series('css:build'));
});

// запуск задач при изменении файлов
gulp.task('watch:js:libs', function(){
    gulp.watch(custom.path.watch.js.libs, gulp.series('js:libs:build'));
});

gulp.task('watch:js:app', function(){
    gulp.watch(custom.path.watch.js.app, gulp.series('js:app:build'));
});

// задача по умолчанию
gulp.task('default', gulp.series(
    // 'build',
    'watch'
));