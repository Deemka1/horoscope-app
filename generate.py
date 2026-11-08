import json
from datetime import datetime
from kerykeion import AstrologicalSubjectFactory

MOON_TEMPLATES = {
    'Aries': {'focus': 'Инициатива и быстрые решения', 'do': 'Начни то, что откладывал', 'avoid': 'Импульсивных трат'},
    'Taurus': {'focus': 'Стабильность и ресурсы', 'do': 'Проанализируй бюджет', 'avoid': 'Рискованных инвестиций'},
    'Gemini': {'focus': 'Коммуникация и обучение', 'do': 'Напиши важное сообщение', 'avoid': 'Поверхностных разговоров'},
    'Cancer': {'focus': 'Эмоции и близкие', 'do': 'Позвони семье', 'avoid': 'Игнорирования чувств'},
    'Leo': {'focus': 'Творчество и признание', 'do': 'Прояви лидерство', 'avoid': 'Эгоцентризма'},
    'Virgo': {'focus': 'Детали и здоровье', 'do': 'Наведи порядок в делах', 'avoid': 'Перфекционизма'},
    'Libra': {'focus': 'Партнерство и баланс', 'do': 'Обсуди конфликт', 'avoid': 'Избегания решений'},
    'Scorpio': {'focus': 'Трансформация и глубина', 'do': 'Разберись в сложной ситуации', 'avoid': 'Манипуляций'},
    'Sagittarius': {'focus': 'Расширение горизонтов', 'do': 'Изучи что-то новое', 'avoid': 'Обещаний, которые не сможешь выполнить'},
    'Capricorn': {'focus': 'Дисциплина и цели', 'do': 'Составь план на месяц', 'avoid': 'Прокрастинации'},
    'Aquarius': {'focus': 'Инновации и свобода', 'do': 'Предложи нестандартное решение', 'avoid': 'Изоляции'},
    'Pisces': {'focus': 'Интуиция и творчество', 'do': 'Займись творческим проектом', 'avoid': 'Иллюзий и самообмана'}
}

MERCURY_RETROGRADE_TEMPLATE = {
    'focus': 'Пересмотр и завершение',
    'do': 'Проверь документы, заверши старые задачи',
    'avoid': 'Подписания контрактов, покупки техники, важных поездок'
}

today = datetime.now()

# Создаем объект на сегодня (Москва, онлайн-поиск отключен, чтобы не было предупреждений)
subject = AstrologicalSubjectFactory.from_birth_data(
    name="Today",
    year=today.year,
    month=today.month,
    day=today.day,
    hour=12,
    minute=0,
    lng=37.6173,
    lat=55.7558,
    tz_str="Europe/Moscow",
    online=False
)

# Правильные атрибуты для актуальной версии kerykeion
moon_sign = subject.moon.sign
mercury_retrograde = subject.mercury.retrograde

horoscope = {}
for sign in MOON_TEMPLATES.keys():
    base = MOON_TEMPLATES[sign].copy()
    if mercury_retrograde:
        base['avoid'] = f"{base['avoid']}. {MERCURY_RETROGRADE_TEMPLATE['avoid']}"
    horoscope[sign.lower()] = base

horoscope['meta'] = {
    'date': today.strftime('%Y-%m-%d'),
    'moon_sign': moon_sign,
    'mercury_retrograde': mercury_retrograde
}

with open('horoscope.json', 'w', encoding='utf-8') as f:
    json.dump(horoscope, f, ensure_ascii=False, indent=2)

print("Гороскоп успешно обновлен.")