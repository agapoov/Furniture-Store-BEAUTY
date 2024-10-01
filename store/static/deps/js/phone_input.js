document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector("#id_phone_number");
    var preferredCountries = ["ru", "by", "kz", "us", 'gb'];

    var iti = window.intlTelInput(input, {
        initialCountry: "ru", // Страна по умолчанию
        separateDialCode: true, // Показывать код страны отдельно
        preferredCountries: preferredCountries,
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js"
    });

    input.addEventListener('blur', function() {
        var number = iti.getNumber();
        iti.setNumber(number);
    });

    input.addEventListener('keypress', function(event) {
        var char = String.fromCharCode(event.which);
        // Разрешить только цифры
        if (!/[0-9]/.test(char)) {
            event.preventDefault();
        }
    });

    input.addEventListener('input', function() {
        // Проверка на длину
        if (input.value.length < 9) {
            // Здесь можно вставить логику, если нужно, например, показать сообщение
            console.log("Введите верный номер телефона.");
        }
    });
});
