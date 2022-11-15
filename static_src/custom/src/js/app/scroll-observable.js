function ScrollObservable() {
    this._observers = [];

    // using RAF as a petty debounce
    let inProgress = false;
    const handler = () => {
        if (inProgress) return;
        inProgress = true;

        window.requestAnimationFrame(() => {
            this._process();

            inProgress = false;
        });
    };

    window.addEventListener('scroll', handler);
}

ScrollObservable.prototype._process = function() {

    const viewportHeight = document.documentElement.clientHeight;
    const documentHeight = document.body.clientHeight;
    const offsetCanvasHero = $('.canvas-hero-block').offset().top;

    const  scrolled = Math.max (
        window.scrollY - offsetCanvasHero,
        window.pageYOffset - offsetCanvasHero,
        document.documentElement.scrollTop - offsetCanvasHero,
        document.body.scrollTop
    );

    const scrolledPercentage = Math.round((100 * (100 * scrolled)) / (documentHeight - viewportHeight)) / 100;

    this.publish(scrolledPercentage);
};

ScrollObservable.prototype.subscribe = function(observer) {
    this._observers.push(observer);
};

ScrollObservable.prototype.publish = function(value) {

    this._observers.forEach(observer => {
        observer.next(value);
    });
};

function ScrollObservableWhy() {
    this._observersWhy = [];

    // using RAF as a petty debounce
    let inProgress = false;
    const handlerWhy = () => {
        if (inProgress) return;
        inProgress = true;

        window.requestAnimationFrame(() => {
            this._process();

            inProgress = false;
        });
    };

    window.addEventListener('scroll', handlerWhy);
}

ScrollObservableWhy.prototype._process = function() {

    const viewportHeight = document.documentElement.clientHeight;
    const documentHeight = document.body.clientHeight;
    const offsetWhy = $('.why').offset().top;

    let scrolled = Math.max (

        window.scrollY - offsetWhy,
        window.pageYOffset - offsetWhy,
        document.documentElement.scrollTop - offsetWhy,
        document.body.scrollTop
    );

    const scrolledPercentageWhy = Math.round((100 * (100 * scrolled)) / (documentHeight - viewportHeight)) / 100;

    this.publish(scrolledPercentageWhy);
};

ScrollObservableWhy.prototype.subscribe = function(observerWhy) {
    this._observersWhy.push(observerWhy);
};

ScrollObservableWhy.prototype.publish = function(value) {
    this._observersWhy.forEach(observerWhy => {
        observerWhy.next(value);
    });
};