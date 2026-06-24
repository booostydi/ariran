// Sticky Navigation
const hero = document.getElementById('hero');
// base.html uses #mainHeader, older code used #stickyNav
const stickyNav = document.getElementById('stickyNav') || document.getElementById('mainHeader');
// CSS class used to toggle filled background
if (stickyNav && !stickyNav.classList.contains('visible')) {
    // keep initial state as-is
}


if (stickyNav && hero) {
    window.addEventListener('scroll', () => {
        const heroBottom = hero.offsetTop + hero.offsetHeight;
        if (window.scrollY > heroBottom - 100) {
            stickyNav.classList.add('visible');
        } else {
            stickyNav.classList.remove('visible');
        }
    });
}



// Fade-in animation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

console.log('Arirang Studio Management System loaded');

// ===== Footer modals: Privacy Policy / Terms =====
(function () {
    const overlay = document.getElementById('modal-overlay');
    const closeBtn = document.getElementById('modal-close');
    const titleEl = document.getElementById('modal-title');
    const contentEl = document.getElementById('modal-content');

    if (!overlay || !closeBtn || !titleEl || !contentEl) return;

    const templates = {
        privacy: {
            title: 'Политика конфиденциальности',
            html: `
                <p>
                    Сервис «АРИРАН» (далее — «Сайт») предоставляет возможность находить студии, бронировать съёмочные помещения и управлять заявками через личный кабинет.
                    Мы уважаем приватность пользователей и обрабатываем данные только в объёме, необходимом для работы сервиса.
                </p>

                <h3>1. Какие данные мы обрабатываем</h3>
                <ul>
                    <li>Контактные данные, которые вы указываете при регистрации (например, email/телефон).</li>
                    <li>Данные аккаунта и профиля (например, имя, сведения для доступа в личный кабинет).</li>
                    <li>Данные бронирований: дата/время, выбранная студия, состав заказа и статус.</li>
                    <li>Технические сведения (например, параметры устройства/браузера), необходимые для корректной работы сайта.</li>
                </ul>

                <h3>2. Для чего мы используем данные</h3>
                <ul>
                    <li>Для оформления и подтверждения бронирований студий.</li>
                    <li>Для работы личного кабинета и управления заказами.</li>
                    <li>Для связи с вами по вопросам бронирований и сервиса.</li>
                    <li>Для улучшения работы сайта и устранения ошибок.</li>
                </ul>

                <h3>3. С кем мы можем делиться данными</h3>
                <p>
                    Мы не продаём персональные данные. В отдельных случаях доступ к данным может требоваться для выполнения обязательств по обслуживанию сервиса (например, для технической поддержки).
                    Мы предпринимаем меры для ограничения доступа и защиты информации.
                </p>

                <h3>4. Как мы защищаем информацию</h3>
                <p>
                    Используются организационные и технические меры безопасности, чтобы снизить риск несанкционированного доступа, изменения, раскрытия или уничтожения данных.
                </p>

                <h3>5. Ваши права</h3>
                <p>
                    Вы можете запросить актуализацию, уточнение или удаление данных в рамках действующих требований законодательства.
                    Для обращения используйте контактные данные, указанные в футере сайта.
                </p>

                <p class="modal-note">
                    Настоящий документ носит информативный характер. При необходимости мы можем обновлять политику по мере развития сервиса.
                </p>
            `
        },
        terms: {
            title: 'Пользовательское соглашение',
            html: `
                <p>
                    Настоящее Пользовательское соглашение регулирует использование сервиса «АРИРАН» — комплекса студийных помещений и онлайн-инструментов для поиска и бронирования.
                    Регистрируясь и/или используя сайт, пользователь принимает условия настоящего соглашения.
                </p>

                <h3>1. Предмет соглашения</h3>
                <p>
                    Сервис предоставляет пользователям функциональность: просмотр каталога студий, оформление заявок на аренду, добавление оборудования (если доступно), управление бронированиями.
                </p>

                <h3>2. Права и обязанности пользователя</h3>
                <ul>
                    <li>Использовать сервис добросовестно и не нарушать работоспособность сайта.</li>
                    <li>Предоставлять достоверные сведения при регистрации и оформлении бронирования.</li>
                    <li>Соблюдать условия бронирования выбранной студии и правила площадки.</li>
                </ul>

                <h3>3. Бронирования и подтверждение</h3>
                <p>
                    Бронирование подтверждается в порядке, установленном на стороне сервиса. Доступность слотов может изменяться в зависимости от загрузки студий.
                    Пользователь отвечает за корректность указанных параметров аренды.
                </p>

                <h3>4. Оплата и расчёты</h3>
                <p>
                    Порядок оплат и выставления счетов определяется в рамках процесса бронирования. В случае вопросов пользователь может обратиться через контакты в футере сайта.
                </p>

                <h3>5. Ответственность сторон</h3>
                <p>
                    Сервис предоставляет доступ к функциональности сайта. При этом мы не гарантируем бесперебойную работу по независящим от нас техническим причинам.
                    Пользователь несёт ответственность за действия в рамках своего аккаунта.
                </p>

                <h3>6. Изменения соглашения</h3>
                <p>
                    Мы можем обновлять условия соглашения. Новая редакция вступает в силу с момента публикации на сайте.
                </p>
            `
        }
    };

    function openModal(key) {
        const tpl = templates[key];
        if (!tpl) return;
        titleEl.textContent = tpl.title;
        contentEl.innerHTML = tpl.html;

        overlay.classList.add('active');
        overlay.setAttribute('aria-hidden', 'false');
        // focus for accessibility
        closeBtn.focus();
    }

    function closeModal() {
        overlay.classList.remove('active');
        overlay.setAttribute('aria-hidden', 'true');
    }

    document.querySelectorAll('[data-modal]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            openModal(link.dataset.modal);
        });
    });

    closeBtn.addEventListener('click', closeModal);

    overlay.addEventListener('click', (e) => {
        // close only when clicking on overlay, not on modal content
        if (e.target === overlay) closeModal();
    });

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
})();


// Fallback: if IntersectionObserver is not supported, reveal fade-in elements
if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
} else {
    // Also reveal any fade-in elements that are already in the viewport on load
    window.addEventListener('load', () => {
        document.querySelectorAll('.fade-in').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) el.classList.add('visible');
        });
    });
}

