const CanvasFrameScrubber = (() => {
    const create = (context, frames) => {
        let currentFrame = 0;

        const observer = {
            next: percentage => {
                let frameIndex;

                if($(window).width() < "992") {
                    frameIndex = Math.floor((percentage * (frames.length - 1)) / 30);
                } else {
                    frameIndex = Math.floor((percentage * (frames.length - 1)) / 50);
                }

                if (currentFrame === frameIndex) return

                if ($(window).scrollTop() > $('.canvas-hero-block').offset().top &&
                    $(window).scrollTop() + window.innerHeight < $('#canvas-hero-end').offset().top) {
                    // положение фреймов от блока
                    window.requestAnimationFrame(() => {
                        context.drawImage(frames[frameIndex], 0, 0);
                    });
                }
            }
        };
        return observer;
    };

    return {
        create: create
    };
})();

const CanvasFrameScrubberWhy = (() => {
    const create = (contextWhy, framesWhy) => {
        let currentFrame = 0;

        const observerWhy = {
            next: percentage => {
                const frameIndex = Math.floor((percentage * (framesWhy.length - 1)) / 43);

                if (currentFrame === frameIndex) return;

                if ($(window).scrollTop() > $('.why').offset().top &&
                    $(window).scrollTop() + window.innerHeight < $('#why-end').offset().top) {
                    // положение фреймов от блока
                    window.requestAnimationFrame(() => {
                        contextWhy.drawImage(framesWhy[frameIndex], 0, 0);
                    });
                }
            }
        };

        return observerWhy;
    };

    return {
        create: create
    };
})();