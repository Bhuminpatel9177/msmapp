/*!
 * jquery.requestanimationframe - 0.2.3-pre
 * https://github.com/gnarf37/jquery-requestAnimationFrame
 * Requires jQuery 1.8+
 *
 * Copyright (c) 2016 Corey Frang
 * Licensed under the MIT license.
 */

;(function($) {
    if (!$ || !$.fn || !$.fn.jquery || Number( $.fn.jquery.split( "." )[ 0 ] ) >= 3 ) {
        return;
    }

    var animating;

    function raf() {
        if ( animating ) {
            window.requestAnimationFrame( raf );
            $.fx.tick();
        }
    }

    if ( window.requestAnimationFrame ) {
        $.fx.timer = function( timer ) {
            if ( timer() && $.timers.push( timer ) && !animating ) {
                animating = true;
                raf();
            }
        };

        $.fx.stop = function() {
            animating = false;
        };
    }

})(window.jQuery);
