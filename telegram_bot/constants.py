ABOUT_TEXT = (
    "\n"
    "\n"
    "В вашем распоряжении два роскошных зала:\n"
    "\n"
    "<b>Кабинетная планировка, 3 этаж</b>\n"
    "Это престижный небольшой разряд, где комфортно размещается"
    " до 23 человек. Зал расположен на 3-м этаже, в левом крыле "
    "здания. Помещение состоит из трех уютных отдельных "
    "кабинетов на 10, 6, и 5 человек. В данном разряде небольшая"
    " парная с отличным паром, всегда наполненная ароматами полыни, "
    "мяты и донника, мыльня с теплыми скамейками из мрамора и "
    "душевыми кабинами; купель с ледяной водой. Так же для Вас "
    "работает бар, где всегда имеется большой выбор различных "
    "закусок, прохладительных напитков, горячий чай. Здесь "
    "всегда царят комфорт и душевная обстановка.\n"
    "\n"
    "Мужские дни:\n"
    "Понедельник, среда, пятница, воскресенье\n"
    "Женские дни:\n"
    "Вторник, четверг, суббота\n"
    "\n"
    "Кабинет на 12 чел.	- 2 часа	1100 руб./чел.\n"
    "Кабинет на 6 чел.	- 2 часа	1150 руб./чел.\n"
    "Кабинет на 5 чел.	- 2 часа	1120 руб./чел.\n"
    "\n"
    "*для льготников с 8:00 до 16:00 (вход до 14:00) 650 руб./ "
    "2 часа\n"
    "дети до 7 лет - бесплатно (Вт; Ср; Чт; Пт;)\n"
    "Помывка в будние дни (при наличии свободных мест) - 1500 "
    "руб./ 3-х часовой сеанс\n"
    "Дети 7-12 лет, пенсионеры, многодетные, участники боевых "
    "действий, инвалиды, ликвидаторы Чернобыльской аварии - "
    "850 руб./ 3-х часовой сеанс\n"
    "\n"
    "\n"
    ""
)

CONTACTS_TEXT = (
    "Наш адрес:\n"
    "6-я Парковая ул., д. 6\n"
    "\n"
    "Часы работы:\n"
    "Понедельник: 14:00—22.00\n"
    "Вторник - воскресенье: 08:00—22:00\n"
    "\n"
    "Наш сайт:\n"
    "https://izmbani.ru/\n"
    "\n"
    "Позвонить:\n"
    "+7 499 165 98 54\n"
    "+7 499 116 30 03\n"
    "+7 916 182 77 77\n"
    "\n"
    "Написать:\n"
    "info@izmbani.ru\n"
    "\n"
    "\n"
)

MONTHS = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}

WEEK_DAYS = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье",
}

SCHEDULE = {
    # Понедельник
    1: {
        # Второй этаж
        2: "мужской",
        # Третий этаж
        3: "мужской",
    },
    # Вторник
    2: {2: "женский", 3: "мужской"},
    # Среда
    3: {2: "мужской", 3: "мужской"},
    # Четверг
    4: {2: "женский", 3: "мужской"},
    # Пятница
    5: {2: "мужской", 3: "мужской"},
    # Суббота
    6: {2: "мужской", 3: "мужской"},
    # Воскресенье
    7: {2: "мужской", 3: "мужской"},
}

START_HOURS = [8, 10, 12, 14, 16, 18, 20, 22]
