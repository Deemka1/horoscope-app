const VERSION = '2026.11.09.5';
let horoscopeData = null;
let currentSign = null;
let currentPeriod = 'today';

const SIGN_NAMES = {
    'aries': 'Овен', 'taurus': 'Телец', 'gemini': 'Близнецы', 'cancer': 'Рак',
    'leo': 'Лев', 'virgo': 'Дева', 'libra': 'Весы', 'scorpio': 'Скорпион',
    'sagittarius': 'Стрелец', 'capricorn': 'Козерог', 'aquarius': 'Водолей', 'pisces': 'Рыбы'
};

const PERIODS = [
    { id: 'today', label: 'День' },
    { id: 'this_week', label: 'Неделя' },
    { id: 'this_month', label: 'Месяц' },
    { id: 'this_year', label: 'Год' }
];

// Загрузка данных
fetch('horoscope.json?v=' + VERSION)
    .then(r => r.json())
    .then(data => { horoscopeData = data; })
    .catch(err => console.error('Ошибка загрузки:', err));

// Навигация между экранами
document.querySelectorAll('.tab-item').forEach(tab => {
    tab.addEventListener('click', () => {
        const screenId = tab.dataset.screen;
        document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById('screen-' + screenId).classList.add('active');
        document.querySelector('.content').scrollTop = 0;
    });
});

// Выбор знака
document.querySelectorAll('.sign-card').forEach(card => {
    card.addEventListener('click', () => {
        document.querySelectorAll('.sign-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        currentSign = card.dataset.sign;
        renderForecast();
    });
});

// Рендер прогноза
function renderForecast() {
    const container = document.getElementById('forecastContainer');
    
    if (!currentSign) {
        container.innerHTML = '';
        return;
    }
    
    if (!horoscopeData) {
        container.innerHTML = '<div class="empty-state">Загрузка данных...</div>';
        return;
    }
    
    let html = '<div class="segmented">';
    PERIODS.forEach(p => {
        const active = p.id === currentPeriod ? 'active' : '';
        html += `<button class="segment ${active}" data-period="${p.id}">${p.label}</button>`;
    });
    html += '</div>';
    
    const data = horoscopeData[currentSign][currentPeriod];
    if (data) {
        html += `
            <div class="forecast-card">
                <div class="forecast-meta">
                    <span class="forecast-date">${SIGN_NAMES[currentSign]} · ${data.date_ref}</span>
                    <span class="forecast-astro">${data.astro_fact}</span>
                </div>
                
                <div class="planet-row venus">
                    <div class="planet-label">Венера</div>
                    <div class="planet-text">${data.venus}</div>
                </div>
                <div class="planet-row mars">
                    <div class="planet-label">Марс</div>
                    <div class="planet-text">${data.mars}</div>
                </div>
                
                <div class="forecast-section" style="margin-top: 18px;">
                    <div class="forecast-label">Фокус периода</div>
                    <div class="forecast-text">${data.focus}</div>
                </div>
                <div class="forecast-section">
                    <div class="forecast-label">Рекомендуется</div>
                    <div class="forecast-text">${data.do}</div>
                </div>
                <div class="forecast-section">
                    <div class="forecast-label">Категорически избегать</div>
                    <div class="forecast-text">${data.avoid}</div>
                </div>
            </div>
            
            <div class="premium-teaser">
                <span class="premium-badge">Скоро</span>
                <h3 class="premium-title">Полный разбор натальной карты</h3>
                <p class="premium-text">
                    Бесплатный гороскоп показывает лишь поверхностные транзиты. 
                    Полный разбор раскроет ваши кармические задачи, сильные стороны и точки роста.
                </p>
                <ul class="premium-features">
                    <li>Все 12 домов гороскопа с детальной интерпретацией</li>
                    <li>Аспекты между планетами и их влияние на судьбу</li>
                    <li>Кармические узлы и задачи воплощения</li>
                    <li>Прогноз на 12 месяцев с точными датами событий</li>
                    <li>Совместимость с партнёром (синастрия)</li>
                </ul>
                <div class="premium-placeholder">Функция в разработке</div>
            </div>
        `;
    }
    
    container.innerHTML = html;
    
    container.querySelectorAll('.segment').forEach(btn => {
        btn.addEventListener('click', () => {
            currentPeriod = btn.dataset.period;
            renderForecast();
        });
    });
}

// Переключение времени
function toggleTimeInput() {
    const isApproximate = document.getElementById('approximateTime').checked;
    document.getElementById('exactTimeBlock').classList.toggle('hidden', isApproximate);
    document.getElementById('approximateTimeBlock').classList.toggle('hidden', !isApproximate);
}

// Расчёт асцендента
async function calculateAscendant() {
    if (!document.getElementById('consentCheckbox').checked) {
        showAscendantError('Подтвердите согласие на обработку данных');
        return;
    }

    const city = document.getElementById('cityInput').value.trim();
    const day = document.getElementById('dayInput').value;
    const month = document.getElementById('monthInput').value;
    const year = document.getElementById('yearInput').value;
    const isApproximate = document.getElementById('approximateTime').checked;
    
    let hour, minute;
    if (isApproximate) {
        [hour, minute] = document.getElementById('timeOfDay').value.split(':');
    } else {
        hour = document.getElementById('hourInput').value;
        minute = document.getElementById('minuteInput').value;
    }

    if (!city || !day || !month || !year) {
        showAscendantError('Заполните все поля');
        return;
    }

    const btn = document.getElementById('calcBtn');
    const resultDiv = document.getElementById('ascendantResult');
    
    btn.disabled = true;
    btn.textContent = 'Считаем...';
    resultDiv.innerHTML = '';

    try {
        const url = `https://astro-calc.fit-for.workers.dev/?city=${encodeURIComponent(city)}&year=${year}&month=${month}&day=${day}&hour=${hour}&minute=${minute}&v=${VERSION}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error('Ошибка сети');
        const data = await response.json();

        if (data.error) {
            showAscendantError(data.error);
        } else {
            const timeLabel = isApproximate ? ' (примерно)' : '';
            resultDiv.innerHTML = `
                <div class="result-card">
                    <h3 class="result-title">Асцендент в знаке ${data.ascendant.sign}</h3>
                    <div class="result-row">
                        <span class="result-label">Градус</span>
                        <span class="result-value">${data.ascendant.degree_in_sign}</span>
                    </div>
                    <div class="result-row">
                        <span class="result-label">Время</span>
                        <span class="result-value">${hour}:${minute}${timeLabel}</span>
                    </div>
                    <div class="result-row">
                        <span class="result-label">Город</span>
                        <span class="result-value">${data.city.split(',')[0]}</span>
                    </div>
                    <div class="result-interpretation">${data.interpretation}</div>
                </div>
            `;
        }
    } catch (error) {
        showAscendantError('Ошибка соединения. Попробуйте позже.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Рассчитать';
    }
}

function showAscendantError(message) {
    document.getElementById('ascendantResult').innerHTML = `<div class="error-msg">${message}</div>`;
}