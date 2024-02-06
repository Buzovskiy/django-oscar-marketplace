// Сборка статики по умолчанию cms django-oscar

/* подключаем gulp и плагины */
var gulp = require('gulp'),  // подключаем Gulp
    plumber = require('gulp-plumber'), // модуль для отслеживания ошибок
    sourcemaps = require('gulp-sourcemaps'), // модуль для генерации карты исходных файлов
    sass = require('gulp-sass')(require('sass')), // модуль для компиляции SASS (SCSS) в CSS
    autoprefixer = require('gulp-autoprefixer') // модуль для автоматической установки автопрефиксов

// пути для стилей по умолчанию cms django-oscar
var path = {
    build: {
        // для файлов админки и стилей по умолчанию
        css: 'static_src/oscar/css/',
    },
    src: {
        // для стилей по умолчанию
        style: 'static_src/oscar/scss/styles.scss',
        // для админки
        style_dashboard: 'static_src/oscar/scss/dashboard.scss',
    },
    watch: {
        // для файлов админки и стилей по умолчанию
        css: 'static_src/oscar/scss/**/*.scss',
    },
}

// сбор стилей cms django-oscar
function css_build(){
    return gulp.src(this.sources)
    .pipe(plumber()) // для отслеживания ошибок
    .pipe(sourcemaps.init()) // инициализируем sourcemap
    .pipe(sass()) // scss -> css
    .pipe(autoprefixer()) // добавим префиксы
    .pipe(gulp.dest(path.build.css))
    .pipe(sourcemaps.write('./')) // записываем sourcemap
    .pipe(gulp.dest(path.build.css)) // выгружаем в build
}


let sources = [path.src.style, path.src.style_dashboard];

module.exports.path = path;
module.exports.cssBuild = css_build.bind({sources: sources});