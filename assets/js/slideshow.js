// Slideshow functionality with Swiper.js
// Dark minimalist carousel for Kushal Samant's portfolio

document.addEventListener('DOMContentLoaded', function() {
  // Check if swiper container exists (homepage only)
  const swiperContainer = document.querySelector('.swiper');
  
  if (swiperContainer) {
    // Initialize Swiper
    const swiper = new Swiper('.swiper', {
      // Fade effect for elegant transitions
      effect: 'fade',
      fadeEffect: {
        crossFade: true
      },
      
      // Auto-play configuration
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true
      },
      
      // Loop through slides
      loop: true,
      
      // Speed of transitions
      speed: 600,
      
      // Navigation arrows
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      
      // Keyboard control
      keyboard: {
        enabled: true,
        onlyInViewport: true,
      },
      
      // Accessibility
      a11y: {
        prevSlideMessage: 'Previous slide',
        nextSlideMessage: 'Next slide',
      },
      
      // Update counter on slide change
      on: {
        init: function () {
          updateCounter(this);
        },
        slideChange: function () {
          updateCounter(this);
        }
      }
    });
    
    // Update counter display
    function updateCounter(swiper) {
      const counterEl = document.querySelector('.slideshow-counter');
      if (counterEl) {
        const realIndex = swiper.realIndex + 1;
        const totalSlides = swiper.slides.length - 2; // Subtract loop duplicates
        counterEl.textContent = `${realIndex}/${totalSlides}`;
      }
    }
  }
});

