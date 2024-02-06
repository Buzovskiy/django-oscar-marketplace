/* подключаем gulp и плагины */
var gulp = require('gulp'),  // подключаем Gulp
    plumber = require('gulp-plumber'), // модуль для отслеживания ошибок
    rigger = require('gulp-rigger'), // модуль для импорта содержимого одного файла в другой
    sourcemaps = require('gulp-sourcemaps'), // модуль для генерации карты исходных файлов
    sass = require('gulp-sass')(require('sass')), // модуль для компиляции SASS (SCSS) в CSS
    autoprefixer = require('gulp-autoprefixer'), // модуль для автоматической установки автопрефиксов
    cleanCSS = require('gulp-clean-css'), // плагин для минимизации CSS
    uglify = require('gulp-uglify'), // модуль для минимизации JavaScript
    cache = require('gulp-cache'), // модуль для кэширования
    imagemin = require('gulp-imagemin'), // плагин для сжатия PNG, JPEG, GIF и SVG изображений
    jpegrecompress = require('imagemin-jpeg-recompress'), // плагин для сжатия jpeg	
    pngquant = require('imagemin-pngquant'), // плагин для сжатия png
    del = require('del'), // плагин для удаления файлов и каталогов
    rename = require('gulp-rename');


var path_to_build = 'static_src/custom/build';
var path_to_src = 'static_src/custom/src';


function copyWebfonts(){
    return gulp.src('static_src/oscar/webfonts/*')
       .pipe(gulp.dest(path_to_build + '/webfonts'))
}
    
/* пути к исходным файлам (src), к готовым файлам (build), а также к тем, 
за изменениями которых нужно наблюдать (watch) */
var path = {
    build: {
        js: {
            app: `${path_to_build}/js/`,
            libs: `${path_to_build}/js/`
        },
        css: `${path_to_build}/css/`,
        img: `${path_to_build}/img/`,
    },
    src: {
        js: {
            app: `${path_to_src}/js/app/app.js`,
            libs: `${path_to_src}/js/libs/libs.js`
        },
        style: `${path_to_src}/style/main.scss`,
        img: `${path_to_src}/img/**/*.*`,
    },
    watch: {
        js: {
            app: `${path_to_src}/js/app/*.js`,
            libs: `${path_to_src}/js/libs/*.js`,
        },
        css: `${path_to_src}/style/**/*.scss`,
        img: `${path_to_src}/img/**/*.*`,
    },
    clean: `./${path_to_build}/*`,
    clean_img: `./${path_to_build}/img/*`
};

/* задачи */

// сбор стилей
function cssBuild(){
    return gulp.src(path.src.style) // получим main.scss
    .pipe(plumber()) // для отслеживания ошибок
    .pipe(sourcemaps.init()) // инициализируем sourcemap
    .pipe(sass()) // scss -> css
    .pipe(autoprefixer()) // добавим префиксы
    .pipe(gulp.dest(path.build.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cleanCSS()) // минимизируем CSS
    .pipe(sourcemaps.write('./')) // записываем sourcemap
    .pipe(gulp.dest(path.build.css)) // выгружаем в build
}

// сбор js библиотек
function jsLibsBuild(){
    return gulp.src(path.src.js.libs) // получим файл libs.js
    .pipe(plumber()) // для отслеживания ошибок
    .pipe(rigger()) // импортируем все указанные файлы в libs.js
    .pipe(gulp.dest(path.build.js.libs))
    .pipe(rename({ suffix: '.min' }))
    .pipe(sourcemaps.init()) //инициализируем sourcemap
     // .pipe(uglify()) // минимизируем js
    .pipe(sourcemaps.write('./')) //  записываем sourcemap
    .pipe(gulp.dest(path.build.js.libs)) // положим готовый файл
    .pipe(gulp.src(`${path_to_src}/js/libs/model-viewer.min.js`))
    .pipe(gulp.dest(path.build.js.libs))
}

// сбор js приложения
function jsAppBuild(){
    return gulp.src(path.src.js.app) // получим файл app.js
    .pipe(plumber()) // для отслеживания ошибок
    .pipe(rigger()) // импортируем все указанные файлы в app.js
    .pipe(gulp.dest(path.build.js.app))
    .pipe(rename({ suffix: '.min' }))
    .pipe(sourcemaps.init()) //инициализируем sourcemap
     // .pipe(uglify()) // минимизируем js
    .pipe(sourcemaps.write('./')) //  записываем sourcemap
    .pipe(gulp.dest(path.build.js.app)) // положим готовый файл
    .pipe(gulp.dest(path.build.js.app))
}

// обработка картинок
function imageBuild(){
    return gulp.src(path.src.img) // путь с исходниками картинок
    .pipe(cache(imagemin([ // сжатие изображений
        imagemin.gifsicle({ interlaced: true }),
        jpegrecompress({
            progressive: true,
            max: 90,
            min: 80
        }),
        pngquant(),
        imagemin.svgo({ plugins: [{ removeViewBox: false }] })
    ])))
    .pipe(gulp.dest(path.build.img)); // выгрузка готовых файлов
}

module.exports.cssBuild = cssBuild;
module.exports.jsLibsBuild = jsLibsBuild;
module.exports.jsAppBuild = jsAppBuild;
module.exports.imageBuild = imageBuild;
module.exports.copyWebfonts = copyWebfonts;
module.exports.path = path;