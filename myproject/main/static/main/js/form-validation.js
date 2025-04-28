document.addEventListener('DOMContentLoaded', function() {
   var phoneField = document.querySelector('[name="telephone"]'); // Получаем поле для телефона

    // Создаем маску для телефона
    var mask = IMask(phoneField, {
        mask: '+{7} (000) 000 00-00',
        lazy: false,
    });



    // Получаем все кнопки toggle для пароля
    var toggleButtons = document.querySelectorAll('.password-toggle');

    // Устанавливаем начальный смайлик и добавляем обработчик события для каждой кнопки
    toggleButtons.forEach(function(button) {
        var targetField = document.querySelector('[name="' + button.getAttribute('data-target') + '"]');

        // Начальный смайлик
        button.textContent = '👁️';

        // Обработчик клика
        button.addEventListener('click', function() {
                if (targetField.type === 'password') {
                    targetField.type = 'text';
                    button.textContent = '🙈'; // Показать обезьянку, если пароль виден
                } else {
                targetField.type = 'password';
                button.textContent = '👁️'; // Вернуть глазик
                }
        });
    });
});
