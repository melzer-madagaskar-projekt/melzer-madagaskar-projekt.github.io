document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.partner-slide');
  const dots = document.querySelectorAll('.dot');
  let current = 0;
  let timer;

  function goTo(index) {
    // Wrap around
    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;

    // Update slides and dots
    slides[current].classList.remove('active');
    dots[current].classList.remove('active');
    slides[index].classList.add('active');
    dots[index].classList.add('active');

    current = index;
  }

  function startTimer() {
    timer = setInterval(() => goTo(current + 1), 15000);
  }

  function resetTimer() {
    clearInterval(timer);
    startTimer();
  }

  // Arrow buttons
  document.querySelector('.slide-nav.prev').addEventListener('click', () => {
    goTo(current - 1);
    resetTimer();
  });

  document.querySelector('.slide-nav.next').addEventListener('click', () => {
    goTo(current + 1);
    resetTimer();
  });

  // Dot buttons
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      goTo(index);
      resetTimer();
    });
  });

  // Start autoplay
  startTimer();
});