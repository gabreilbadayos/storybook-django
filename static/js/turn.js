/**
 * Custom Flipbook Implementation
 * A lightweight flipbook effect for PDF viewing on desktop
 * Uses CSS transforms and transitions for realistic page flip animation
 */

(function($) {
    'use strict';

    var Flipbook = function(element, options) {
        this.element = $(element);
        this.options = $.extend({}, Flipbook.DEFAULTS, options);
        this.currentPage = 1;
        this.totalPages = this.options.pages;
        this.isAnimating = false;
        
        this.init();
    };

    Flipbook.DEFAULTS = {
        width: 800,
        height: 600,
        page: 1,
        pages: 1,
        autoCenter: true,
        display: 'double',
        acceleration: true,
        gradients: true,
        elevation: 50,
        duration: 1000,
        when: {}
    };

    Flipbook.prototype.init = function() {
        var self = this;
        
        this.element.css({
            'position': 'relative',
            'width': this.options.width,
            'height': this.options.height,
            'perspective': '2000px'
        });
        
        this.createPages();
        this.bindEvents();
        
        if (this.options.autoCenter) {
            this.element.css({
                'margin': '0 auto'
            });
        }
        
        if (this.options.page > 1) {
            this.turnToPage(this.options.page);
        }
    };

    Flipbook.prototype.createPages = function() {
        var pages = this.element.find('.turn-page');
        
        pages.each(function(index) {
            var pageNum = index + 1;
            var $page = $(this);
            
            $page.css({
                'position': 'absolute',
                'width': '50%',
                'height': '100%',
                'top': 0,
                'left': pageNum % 2 === 0 ? '50%' : 0,
                'transform-style': 'preserve-3d',
                'backfaceVisibility': 'hidden'
            });
            
            if (pageNum % 2 === 0) {
                $page.css({
                    'transform-origin': 'left center'
                });
            } else {
                $page.css({
                    'transform-origin': 'right center'
                });
            }
        });
    };

    Flipbook.prototype.bindEvents = function() {
        var self = this;
        
        this.element.on('click', '.turn-page', function() {
            var pageNum = $(this).data('page');
            if (pageNum < self.currentPage) {
                self.previous();
            } else if (pageNum > self.currentPage) {
                self.next();
            }
        });
    };

    Flipbook.prototype.next = function() {
        if (this.currentPage < this.totalPages && !this.isAnimating) {
            this.turnToPage(this.currentPage + 1);
        }
    };

    Flipbook.prototype.previous = function() {
        if (this.currentPage > 1 && !this.isAnimating) {
            this.turnToPage(this.currentPage - 1);
        }
    };

    Flipbook.prototype.turnToPage = function(page) {
        var self = this;
        var oldPage = this.currentPage;
        
        if (page < 1 || page > this.totalPages) return;
        
        this.isAnimating = true;
        this.currentPage = page;
        
        var $currentPage = this.element.find('[data-page="' + page + '"]');
        
        if (page % 2 === 0) {
            $currentPage.css({
                'transform': 'rotateY(-180deg)',
                'transition': 'transform ' + this.options.duration + 'ms',
                'z-index': 10
            });
        } else {
            $currentPage.css({
                'transform': 'rotateY(180deg)',
                'transition': 'transform ' + this.options.duration + 'ms',
                'z-index': 10
            });
        }
        
        setTimeout(function() {
            self.isAnimating = false;
            
            if (self.options.when && self.options.when.turning) {
                self.options.when.turning(null, page, [page]);
            }
            
            if (self.options.when && self.options.when.turned) {
                self.options.when.turned(null, page, [page]);
            }
        }, this.options.duration);
        
        if (this.options.when && this.options.when.turning) {
            this.options.when.turning(null, page, [page]);
        }
    };

    Flipbook.prototype.size = function(width, height) {
        this.options.width = width;
        this.options.height = height;
        
        this.element.css({
            'width': width,
            'height': height
        });
    };

    Flipbook.prototype.destroy = function() {
        this.element.off('click');
        this.element.find('.turn-page').remove();
        this.element.removeData('flipbook');
    };

    $.fn.flipbook = function(option) {
        var args = Array.prototype.slice.call(arguments, 1);
        
        return this.each(function() {
            var $this = $(this);
            var data = $this.data('flipbook');
            var options = typeof option === 'object' && option;
            
            if (!data) {
                $this.data('flipbook', (data = new Flipbook(this, options)));
            }
            
            if (typeof option === 'string') {
                data[option].apply(data, args);
            }
        });
    };

    $.fn.flipbook.Constructor = Flipbook;

})(jQuery);
