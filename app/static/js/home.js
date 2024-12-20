
    var carousel = document.getElementById('carouselExampleFade');
    var carouselItems = carousel.querySelectorAll('.carousel-item');
    var interval = 2000;
  
    function autoTransition() {
      var currentIndex = carousel.querySelector('.active').getAttribute('data-bs-slide-to');
      var nextIndex = (currentIndex + 1) % carouselItems.length;
      carousel.querySelector(`[data-bs-slide-to="${nextIndex}"]`).click();
    }
  
    setInterval(autoTransition, interval);
