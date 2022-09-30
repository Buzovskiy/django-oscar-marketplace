if (document.querySelector('.canvas-hero-block')) {

    (async () => {

        startProgress();

        let videoContainer;
        let framesUrlElement;

        if($(window).width() < "992") {
            videoContainer = document.querySelector('#canvasHeroMob');
            framesUrlElement = document.querySelector('input[name="frames-url-mob"]');
        } else {
            videoContainer = document.querySelector('#canvasHeroPC');
            framesUrlElement = document.querySelector('input[name="frames-url-pc"]');
        }

        if (!videoContainer || !framesUrlElement) {
            throw new Error('Element missing!');
        }

        const framesUrlPattern = framesUrlElement.value;
        const framesUrlStart = parseInt(framesUrlElement.dataset.frameStart, 10);
        const framesUrlEnd = parseInt(framesUrlElement.dataset.frameEnd, 10);
        const framesIdPadding = parseInt(framesUrlElement.dataset.frameIdPadding, 10);

        log(`Initializing frames download...`);

        log(`Please be patient. Downloaing ${framesUrlEnd} frames...`);

        const startTime = Date.now();

        const frames = await FrameUnpacker.unpack({
            urlPattern: framesUrlPattern,
            start: framesUrlStart,
            end: framesUrlEnd,
            padding: framesIdPadding
        });

        const endTime = Date.now();

        log(`Took ${(endTime - startTime) / 1000} seconds.`);

        log('Painting canvas with first frame...');

        const canvas = document.createElement('canvas');
        canvas.classList.add('canvas');
        canvas.height = frames[0].height;
        canvas.width = frames[0].width;
        const context = canvas.getContext('2d');
        context.drawImage(frames[0], 0, 0);

        videoContainer.appendChild(canvas);

        log('Setting up scrubber...');

        const observer = CanvasFrameScrubber.create(context, frames);

        const observable = new ScrollObservable();
        observable.subscribe(observer);

        log('Ready! Scroll to scrub.');

        stopProgress();


        /* Preloader */
        const preloader = document.querySelector('.preloader')

        preloader.classList.add('preloader__hidden')

        setTimeout(
            function(){
                let scrollTopCanvas;
                if($(window).width() < "992") {
                    scrollTopCanvas = 500;
                } else {
                    scrollTopCanvas = 2500;
                }
                $('html, body').animate({scrollTop: scrollTopCanvas},2000);
            },
            1500
        );
    })();

}

if (document.querySelector('.why')) {

    (async () => {

        startProgress();

        const videoContainerWhy = document.querySelector('#canvasWhy');
        const framesUrlElementWhy = document.querySelector('input[name="frames-url-why"]');
        if (!videoContainerWhy || !framesUrlElementWhy) {
            throw new Error('Element missing!');
        }

        const framesUrlPatternWhy = framesUrlElementWhy.value;
        const framesUrlStartWhy = parseInt(framesUrlElementWhy.dataset.frameStart, 10);
        const framesUrlEndWhy = parseInt(framesUrlElementWhy.dataset.frameEnd, 10);
        const framesIdPaddingWhy = parseInt(framesUrlElementWhy.dataset.frameIdPadding, 10);

        log(`Initializing frames download...`);

        log(`Please be patient. Downloaing ${framesUrlEndWhy} frames...`);

        const startTimeWhy = Date.now();

        const framesWhy = await FrameUnpackerWhy.unpackWhy({
            urlPattern: framesUrlPatternWhy,
            start: framesUrlStartWhy,
            end: framesUrlEndWhy,
            padding: framesIdPaddingWhy
        });

        const endTimeWhy = Date.now();

        log(`Took ${(endTimeWhy - startTimeWhy) / 1000} seconds.`);

        log('Painting canvas with first frame...');

        const canvasWhy = document.createElement('canvas');
        canvasWhy.classList.add('canvas');
        canvasWhy.height = framesWhy[0].height;
        canvasWhy.width = framesWhy[0].width;
        const contextWhy = canvasWhy.getContext('2d');
        contextWhy.drawImage(framesWhy[0], 0, 0);

        videoContainerWhy.appendChild(canvasWhy);

        log('Setting up scrubber...');

        const observerWhy = CanvasFrameScrubberWhy.create(contextWhy, framesWhy);

        const observableWhy = new ScrollObservableWhy();
        observableWhy.subscribe(observerWhy);

        log('Ready! Scroll to scrub.');

        stopProgress();
    })();
}