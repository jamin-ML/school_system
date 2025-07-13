// Initialize components when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Mobile sidenav
            M.Sidenav.init(document.querySelectorAll('.sidenav'), {edge: 'left'});
            
            // Slider
            M.Slider.init(document.querySelectorAll('.slider'), {
                indicators: false,
                height: 500,
                duration: 500,
                interval: 5000
            });
            
            // ScrollSpy
            M.ScrollSpy.init(document.querySelectorAll('.scrollspy'));
            
            // Material Box (for images)
            M.Materialbox.init(document.querySelectorAll('.materialboxed'));
            
            // Initialize animations
            setTimeout(function() {
                // Animate features on scroll
                const features = document.querySelectorAll('.feature-card, .step-number, .testimonial-card');
                const options = {
                    threshold: 0.01
                };
                
                const observer = new IntersectionObserver(function(entries, observer) {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('animated');
                            observer.unobserve(entry.target);
                        }
                    });
                }, options);
                
                features.forEach(feature => {
                    observer.observe(feature);
                });
            }, 100);
        });
            // Initialize components when DOM is loaded
            document.addEventListener('DOMContentLoaded', function() {
                // Mobile sidenav
                M.Sidenav.init(document.querySelectorAll('.sidenav'));
                
                // Chips for filtering
                M.Chips.init(document.querySelectorAll('.chips'), {
                    placeholder: 'Filter by grade',
                    secondaryPlaceholder: '+Grade level'
                });
                
                // Tooltips
                M.Tooltip.init(document.querySelectorAll('.tooltipped'));
                
                // Floating Action Button
                var elems = document.querySelectorAll('.fixed-action-btn');
                M.FloatingActionButton.init(elems, {
                    direction: 'left'
                });
            });