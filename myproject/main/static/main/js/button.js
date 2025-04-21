// Находим кнопку
const btn = document.querySelector('.btn-up');

// Слушаем прокрутку
window.addEventListener('scroll', function() {
  if (window.scrollY > 400) {
    btn.classList.remove('btn-up_hide'); // Показываем кнопку
  } else {
    btn.classList.add('btn-up_hide'); // Прячем кнопку
  }
});

// Слушаем клик по кнопке
btn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // Плавно вверх
  });
});
