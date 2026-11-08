import json
from datetime import datetime, timedelta
from kerykeion import AstrologicalSubjectFactory

# Базовые фактологические рекомендации для знаков
BASE_ADVICE = {
    'Aries': {'focus': 'Инициатива и запуск процессов', 'do': 'Действуй первым, бери ответственность', 'avoid': 'Импульсивных решений и споров'},
    'Taurus': {'focus': 'Ресурсы и стабильность', 'do': 'Планируй бюджет, наводи порядок в делах', 'avoid': 'Рискованных финансовых операций'},
    'Gemini': {'focus': 'Коммуникация и информация', 'do': 'Учись, пиши, договаривайся', 'avoid': 'Поверхностных суждений и сплетен'},
    'Cancer': {'focus': 'Эмоции и близкий круг', 'do': 'Удели время семье, восстанови силы', 'avoid': 'Игнорирования своих потребностей'},
    'Leo': {'focus': 'Творчество и самовыражение', 'do': 'Прояви лидерство, заяви о себе', 'avoid': 'Эгоцентризма и драматизации'},
    'Virgo': {'focus': 'Анализ и систематизация', 'do': 'Детализируй планы, проверь документы', 'avoid': 'Чрезмерной критики и перфекционизма'},
    'Libra': {'focus': 'Партнерство и баланс', 'do': 'Ищи компромиссы, заключай соглашения', 'avoid': 'Избегания прямых ответов'},
    'Scorpio': {'focus': 'Трансформация и глубина', 'do': 'Разбирайся в сути, закрывай старые гештальты', 'avoid': 'Манипуляций и скрытности'},
    'Sagittarius': {'focus': 'Расширение горизонтов', 'do': 'Изучай новое, строй долгосрочные планы', 'avoid': 'Необоснованного оптимизма и обещаний'},
    'Capricorn': {'focus': 'Дисциплина и статус', 'do': 'Работай на результат, укрепляй авторитет', 'avoid': 'Прокрастинации и выгорания'},
    'Aquarius': {'focus': 'Инновации и независимость', 'do': 'Предлагай нестандартные решения, нетворкинг', 'avoid': 'Изоляции и упрямства'},
    'Pisces': {'focus': 'Интуиция и завершение циклов', 'do': 'Слушай внутреннюю оценку, отдыхай', 'avoid': 'Иллюзий и ухода от реальности'}
}

def get_astro_data(days_offset):
    """Рассчитывает реальные астрономические данные на указанную дату"""
    target_date = datetime.now() + timedelta(days=days_offset)
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="Future", year=target_date.year, month=target_date.month, day=target_date.day,
        hour=12, minute=0, lng=37.6173, lat=55.7558, tz_str="Europe/Moscow", online=False
    )
    return {
        "moon_sign": subject.moon.sign,
        "mercury_retrograde": subject.mercury.retrograde,
        "date_str": target_date.strftime('%d.%m.%Y')
    }

# Периоды для расчета (в днях от сегодня)
PERIODS = {
    "today": 0,
    "tomorrow": 1,
    "this_week": 7,
    "next_week": 14,
    "this_month": 30,
    "next_month": 60,
    "this_year": 365
}

horoscope = {}

for sign, advice in BASE_ADVICE.items():
    sign_data = {}
    for period_name, days_offset in PERIODS.items():
        astro = get_astro_data(days_offset)
        
        # Формируем фактологический текст
        mercury_status = "ретроградный ⚠️" if astro["mercury_retrograde"] else "прямой ✅"
        
        focus_text = f"{advice['focus']}."
        do_text = f"{advice['do']}."
        avoid_text = f"{advice['avoid']}."
        
        # Если Меркурий ретроградный в этот период, добавляем фактологическое предупреждение
        if astro["mercury_retrograde"]:
            avoid_text += " В период ретроградного Меркурия критически важно перепроверять документы, не начинать новых глобальных проектов и не делать крупных покупок."

        sign_data[period_name] = {
            "date_ref": astro["date_str"],
            "astro_fact": f"Луна в знаке {astro['moon_sign']}, Меркурий {mercury_status}",
            "focus": focus_text,
            "do": do_text,
            "avoid": avoid_text
        }
    
    horoscope[sign.lower()] = sign_data

# Добавляем метаданные на сегодня для общего отображения
today_astro = get_astro_data(0)
horoscope['meta'] = {
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'current_moon': today_astro['moon_sign'],
    'current_mercury_rx': today_astro['mercury_retrograde']
}

with open('horoscope.json', 'w', encoding='utf-8') as f:
    json.dump(horoscope, f, ensure_ascii=False, indent=2)

print("Фактологический гороскоп на 7 периодов успешно сгенерирован.")