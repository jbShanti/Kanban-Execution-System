---
kanban-plugin: board
created: 2024-11-24T13:39
updated: 2026-06-03T21:14
Processing: "[[Промпт для обработки доски Doing Kanban v1.2]]"
Analytics: "[[Аналитический отчёт по доске Kanban]]"
Homepage: true
state: "[[Focus]]"
Links:
  - "[[Проекты (Homepage)]]"
  - "[[Archived tasks (KB)]]"
  - "[[Backlog Kanban]]"
Status: PLANNING
LLM Prompt: "Задача: Проведи аналитику предоставленной канбан-доски в формате Markdown и представь результат в виде таблицы, выводов и рекомендаций.\r\r

  Контекст: Дата для анализа - сегодня. Выполненная задача всегда помечается как \"- [x]\", положение в секциях или разделах при этом не имеет значения.\ 

  Особые пометки: ❗- задачи с наивысшим вниманием и приоритетом,  🔴 - приоритетные и срочные задачи, 🟠 - приоритетные несрочные задачи, 🟢 - неприоритетные и несрочные задачи.

  Теги: #Priority/Highest - задачи с максимальным приоритетом, #Priority/High - задачи с высоким приоритетом. Также задачи могут быть помечены атрибутом [priority::] для фиксации приоритета.

  Исходные данные: Текст данного файла в формате Markdown, размеченный под формат канбан-доски. Файлы с канбан-доской и задачами, переданные ранее, игнорируй.

  Статус задач:

  - '- [ ]' - активная (открытая) задача

  - '- [х]' - завершённая задача

  - '- [/]' - задача в процессе выполнения

  - '- [-]' - отменённая задача.

  - '- [<]' - задача, которая находится в режиме планирования. Другими словами пока на паузе, в ожидании определения сроков реализации.

  Разделы: все задачи разбиты на разделы (колонки), объединяющих задачи в набор по одной теме или в проект. В названии некоторых колонок (разделов) в скобках указан лимит WIP. У некоторых колонок (разделов) также есть приоритет в формате [P::5], где 5 - наивысший, 1 - наименьший. Учитывай этот приоритет при определении или анализе [score] у задач, в том числе в рекомендациях по переносу задач из одного коридора score в другой.


  Определение архивированных задач:\r

  - Архивированные задачи находятся ТОЛЬКО в разделе \"## Archive\", который в свою очередь находится после разделителя \"***\".

  - Задачи в этом разделе считаются архивированными НЕЗАВИСИМО от их статуса выполнения.

  - Если задача архивирована с пометкой \"Выполнена\", значит она была завершена прежде, чем была архивирована.

  - Архивированная задача — также это любая строка задачи (начинающаяся с `- [`), в конце которой следует разделитель архива в формате ` || ` (двойная вертикальная черта, окружённая пробелами).\r

  - Пример архивированной задачи: `- [x] Task name #tag [score::15]  ||  2026-01-28 14:26`\r- Все задачи с таким разделителем считаются архивированными НЕЗАВИСИМО от их расположения в файле (даже если они находятся вне секции \"Archive\").\r

  - Архивированные задачи учитываются ТОЛЬКО в столбце «Архивировано» аналитической таблицы, даже если они помечены как выполненные (`- [x]`).

  - Не используй другие методы определения архивированных задач (например, поиск по \"||\").

  \r

  Требования к анализу:\r

  \r\r- Перепроверь данный промпт на изменения относительно прежней версии, прежде чем запускать сами действия.

  - Учёт задач:

  -- Анализируй только задачи верхнего уровня (родительские элементы списка). Подзадачи внутри чек-листов и вложенные пункты MUST BE игнорированы.

  -- Задачи из секций \"Done\" и \"Archived\" учитывать только при создании аналитической таблицы.\ 

  -- Если задача архивирована (независимо от статуса её выполнения), то она учитывается только в столбце \"Архивировано\" и не учитывается в столбце \"Выполнено\".

  - Фильтрация: Исключи из анализа задачи, находящиеся в секциях «Goals 2025». Задачи с атрибутом [analytics::ignore] игнорировать в аналитике и рекомендациях.


  Определение статуса относительно текущей даты:

  \r\r\r- Просроченные: Задачи с атрибутом дедлайна (@{YYYY-MM-DD}) или аналогичным (например, [due::] и [scheduled::]), дата которого строго раньше чем сегодня (дата анализа).\r\r\r

  - Активные: Все остальные задачи (не имеющие дедлайна ИЛИ имеющие дедлайн, равный сегодня или позже).

  - На паузе: Задачи со статусом планирования - [<]\r\r\r


  Параметры таблицы анализа задач:

  - Таблица со строгой структурой: «Интервал Score», «Просроченные», «Активные», «Выполнено», «Архивировано», «Итого», «Доля активных задач».

  - Группировка по Score: Разбей все задачи на строки по следующим интервалам атрибута [score::X]:\r\r

  -- 21 - 25 (цель: 3 - 5 активных задач в диапазоне)

  \r\r\r-- 16 - 20 (цель: 6 - 10 активных задач в диапазоне)

  \r\r\r-- 11 - 15 (цель: 11 - 20 активных задач в диапазоне)

  \r\r\r-- 6 - 10 (цель: 21 - 30 активных задач в диапазоне)

  \r\r\r-- 1 - 5  (цель: до 5 активных задач в диапазоне)

  \r\r\r-- 0

  \r\r\r-- Без score (задачи, у которых атрибут score отсутствует)

  - Цель: укажи целевое количество для задач в данном интервале\r\r\r

  - Итого: общее количество задач (цель: от 60 до 70 активных задач на доске)\r\r

  - Расчёт долей: Для каждой строки рассчитай «Долю активных задач» как: (Активные / Итого) * 100%. Результат округли до одного знака после запятой.


  Требования к описанию задач в Inbox:

  - Для задач из Inbox подготовь один Markdown блок для вставки в файл, чтобы каждая задача была отформатирована под md.

  - Перед названием задачи проставь самый подходящий для неё эмодзи, например, но не ограничиваясь: ❗ 🔴 🟠 🟢 ⏰ ⚠️ 🚨 🛠 🔄 ⏳ 🚧 ✅.

  - Пример параметров задачи: - [ ] 📃 Create wishlist for myself [[Список подарков]] #Personal #SelfCare #Family @{2026-04-10} [score::11] [timе::30m] [finance::free]

  - Если в оригинале задачи была ссылка на внутренний в формате \"[[Описание ссылки]]\" или внешний источник в формате \"[Описание ссылки](ссылка на внешний источник)\", то обязательно её сохранить в новой версии, сохранив описание ссылки и саму ссылку в оригинальной форме.

  - Если для задачи не указано примерное время её выполнения (параметр [time::]), то спрогнозируй объем времени, необходимый на её выполнение.

  - Если задача требует покупки товаров или оплаты услуг, то узнай примерную стоимость в рублях и укажи в параметре [cost::]

  - Форматирование\ 


  Ожидаемый результат:

  \r\r\r- Исходные данные: укажи дату, используемую для анализа сроков и статусов задач.

  - Если в разделе \"Inbox\" есть задачи, кроме игнорируемых, то предложи свои формулировки (текст задачи обязательно переведён на английский) и параметры задачи, включая, но не ограничиваясь плановой датой, тегом, score. Ориентируйся на требования к описанию задач в Inbox. Задачи из Inbox, после проставления в них дата выполнения, должны также учитываться в последующих отчётах, включая матрицу выполнения задач на сегодня.

  \r- Таблица анализа задач: Чётко оформленная Markdown-таблица с результатами анализа.\r\r\r

  - Выводы: После таблицы предоставь 3-4 ключевых вывода, основанных на данных из таблицы. Выводы должны отвечать на вопросы: \"Что означают эти цифры?\", \"Какие основные проблемы видно?\".

  \r- Матрица решений на сегодня:\ 

  -- Суть - список из пяти критических задач с явными критериями их выбора. Формат вывода матрицы:

  | Задача | Score | Дедлайн | ~Время | Блокирует что-то? | Рекомендация |

  -- При формировании матрицы учитывай:

  ---  (а) задачи с необратимыми последствиями при просрочке — в приоритете;

  ---  (б) задачи, блокирующие другие задачи — выше несвязанных;

  ---  (в) задачи с [time::] ≤ 15m — предпочтительны при насыщенном дне.

  -- Матрица решений должна формироваться только из:

  --- задач с дедлайном на сегодня,

  --- просроченных задач;

  --- задач с дедлайном ≤ 3 дней;

  --- Активных задач

  --- Задач в In Progress

  - Матрица критических решений (Critical Awareness Matrix)\r

  -- Назначение: выявить 3–7 задач, проектов или обязательств, которые оказывают наибольшее влияние на будущее состояние системы и требуют удержания внимания пользователя независимо от того, будут ли они выполняться сегодня.\r

  -- Матрица критических решений НЕ является планом дня.\r

  -- Критерии отбора (в порядке приоритета):\r

  --- 1. Задачи с необратимыми последствиями при просрочке (здоровье, финансы, юридические вопросы, карьера).\r

  --- 2. Задачи, блокирующие выполнение других задач или целых направлений.\r

  --- 3. Задачи, связанные с ключевыми стратегическими целями пользователя.\r

  --- 4. Задачи, требующие предварительной подготовки, согласований или накопления ресурсов.\r

  --- 5. Задачи с высоким Score (21–25), если они соответствуют одному из критериев выше.\r

  -- Формат вывода:\r

  | Объект внимания | Тип (Health / Finance / Career / Project) | Горизонт | Причина включения | Следующий шаг |\r

  | --------------- | ----------------------------------------- | -------- | ----------------- | ------------- |\r

  --- Горизонт:

  ---- * A — требует действий в течение 72 часов;\r

  ---- * B — требует подготовки в течение недели;\r

  ---- * C — требует регулярного мониторинга;\r

  ---- * D — удерживать в поле зрения.\r

  -- В матрицу допускается включать задачи без дедлайна на сегодня. Основная цель матрицы — ответить на вопрос: «Что сейчас определяет моё будущее состояние и что нельзя потерять из поля зрения?»\r

  - Определи средние показатели закрытия задач за последнее время.

  - Определи максимальное количество задач для выполнения на сегодня, в том опираясь на контекст дня, день недели и так далее. Если на сегодня запланировано более предлагаемого максимального количества задач, то предложи для переноса \"лишние\" задачи с дедлайном на сегодня, предлагай другие дни с учётом имеющихся планов по датам.


  - Динамика системы: Выведи таблицу изменений: ↑/↓ по каждому диапазону, изменение числа просроченных, скорость закрытия задач\ 

  \  (выполнено + архивировано за период) относительно данных предыдущего отчёта.

  - Рассчитай Health Index системы (0–100) по следующим правилам:

  \  Начальное значение: 100.

  \  Штрафы:

  \  -- каждая просроченная задача: −5

  \  -- каждая задача меньше 3 штук в диапазоне 21-25: −5

  \  -- каждая задача сверх 5 штук в диапазоне 21-25: −3

  \  -- каждая задача сверх 10 штук в диапазоне 16-20: −2

  \  -- каждая задача больше 20 штук в диапазоне 11-15: −2

  \  -- каждая задача больше 30 штук в диапазоне 6-10: −2

  \  -- каждая задача больше 5 штук в диапазоне 1-5: −1

  \  -- каждая задача без score в Inbox дольше 48ч: −1

  \  Бонусы:

  \  -- выполнено сегодня ≥ 3 задачи: +5. Учитывать выполненные как в разделе Done, так и в разделе Archive

  \  -- нулевые просрочки: +5

  \  -- диапазон 21-25 в коридоре 3-5: +3

  \ \ 

  \  Выведи итоговый индекс и одну строку интерпретации:

  \  90–100: Система в отличной форме · 70–89: Рабочий режим ·\ 

  \  50–69: Требует внимания · <50: Критическое состояние.


  Если зафиксировано превышение количества задач в заданном интервале Sсore или же задач в коридоре меньше заданной цели, то предложи (выбери) кандидаты на перенос для каждого интервала, указав как текущий указанный для задача Score, так и предлагаемый с обоснованием для каждой задачи.


  Если зафиксирован выход количества активных задач из целевого количественного диапазона, то предложи добавить задачи на доску из бэклога (отдельная доска) или предложи кандидатов для переноса в Backlog. Для каждой предложенной задачи предложи обоснование.


  - Рекомендации по ведению учёта задач:\r

  --  (а) Тактические (сделать сегодня): 1–2 конкретных действия по улучшению \r

  \      состояния доски прямо сейчас. Формат: \"Сделать X → результат Y\".\r

  --  (б) Стратегические (внедрить как привычку): 1–2 системных изменения, \r

  \      которые улучшат планирование на неделях вперёд. \r

  \      Формат: \"Ввести правило: [правило] → это предотвратит [проблему]\".\r


  Ограничения:

  - Исключить из рекомендаций использования одного типа (формата) дедлайнов, поскольку разные форматы используются разными плагинами.


  Другие особенности:\r

  - Контекст дня (опционально): пользователь может передать строку  \"Контекст дня: [локация, доступные ресурсы, ограничения]\", например:   \"Контекст дня: перелёт 6ч, нет интернета, только телефон\".   Если контекст передан — учитывай его при формировании рекомендаций:  не рекомендуй задачи, требующие ресурсов, которых нет. Ожидаемый результат (весь отчёт) при этом также необходимо сформировать полностью.

  - при насыщенном дне приоритет задачам ≤15m.

  - при днях с вечерними fixed-context activities execution capacity автоматически уменьшается на 30–40% → это предотвратит скрытый overload.

  - утренний tactical report должен учитывать не только рабочие часы, но и transportation load → это предотвратит ошибочную оценку доступной энергии.

  - Tasks with [tracking::external]:

  -- should not be included into daily execution recommendations;

  -- should not count as execution overload;

  -- should still count for deadline monitoring;

  -- may appear in strategic reviews only;

  -- should be added to day priority matrix only on it's due date.


  Финальная проверка:

  - Прежде чем подавать результат необходимо перепроверить:

  -- Количество задач в файле и соответствует ли оно количеству задач в аналитической таблице

  -- Другие аналитические показатели на соответствие реальным данным в файле.

  -- Что все шаги из ожидаемого результата выполнены."
---

## ℹ️ INFO

- [i] ❣ Emoji Catalogue:
	❗ 🔴 🟠 🟢 ⏰ ⚠️ 🚨 🛠 🔄 ⏸ ⏳ 🚧 ✅ 📍#Admin/Settings[score::0] [time::0] [finance::skipped] [analytics::ignore]
- [ ] 📍: [[Манифест моего состояния на ближайшие 3 месяца]] [analytics::ignore] @{2026-06-07}
- [ ] 📍: 🥗 [[Рацион на 7 дней]] #Health/Nutrition #Regular [score::12] [time::20m] [finance::free] [analytics::ignore]


## 📬 Inbox



## 🏃 DOING (2)

- [/] 💻 Write a Kanban board parser script #Dev/Tools #Projects/KanbanParser #Regular @{2026-06-03} [score::21] [time::3h] [finance::free]
- [ ] 🟢 Next step on project: [[Оформить и подготовить участок отца к продаже (KB)]]  [score::14] #Projects/FathersLand #Priority/High  #Regular [finance::planned] @{2026-06-03} [time::15m]


## 🗓️ TODAY (3)

- [ ] 📄 Найти мануал для Отца для Maxvi K28 #Family #Subject/Father [score::20] @{2026-06-03}
- [ ] 🟠  Make a [[Monthly report on family expenses]] #Regular #Finance/Reports #Family #Family/Finances #Priority/Highest @{2026-06-03} [finance::free] [score::11]  [time::90m]  [priority:: highest]  [repeat:: every month]  [scheduled:: 2026-06-01]
- [ ] 🫒 Buy unrefined extra virgin olive oil #Health/Nutrition #Shopping @{2026-06-03} [score::9] [time::15m] [cost::700]


## 📝 TO DO (5)

- [/] 🟠 Sort out photos and videos at my phone #Photos/Sorting #Photos/Download  #Regular  [score::6] [continue_date::28-06-2025] [time::1h] @{2026-06-03}  [repeat:: every day when done]  [scheduled:: 2026-04-01]
- [ ] 🟢 Get a Genetic Therapist Consultation – It’s included in your DNA test @{2026-06-03} #Health #Health/Physical [score::8]


## 🔶 MEDIUM PRIORITY FOCUS (5)



## ⏰ CONTROL, DEADLINES, AWAIT (10)

- [ ] ❗Pay for lights and utilities (communal bills) for flat in Moscow #Family/Finances #Regular  @{2026-06-04}  [score::10] [finance::regular]  [repeat:: every month]  [scheduled:: 2026-05-20]
- [ ] 🚭 Give up smoking ([[Памятка курильщику]]) #SelfDevelopment #Health/Physical @{2026-06-21} [score::23]
- [x] 🧪 Take a fecal occult blood test #Health/Physical #Priority/High @{2026-06-02} [score::17] [time::30m] [finance::free]  [completion:: 2026-06-03]
- [ ] 🚨 Buy [[Laptop headphones]] (after first income) #Priority/High #Tech #Buy #Shopping/Technics #Delegated/Before    [score::10] [category::Buying] @{2026-06-06}


## 🎯 Goals (10)

- [ ] (+) Get MYSELF in shape in terms of weight and muscle structure: 73kg #MyGoals/2025 #MyGoals/2025/MyForm  #Health/Physical  ([[Мои цели и планы на 2025 год]]) @{2026-08-01} [finance::free]  [score::10] [category::Goal]
- [ ] (+) Financial freedom via Remote Work ([[Три основные цели на 2026]]) #MyGoals #MyGoals/2026 #MyGoals/2026/FinancialFreedom  @{2026-07-13} [score::10]
- [ ] (+) Mental and Physical Health ([[Три основные цели на 2026]]) #MyGoals #MyGoals/2026 #MyGoals/2026/Health @{2026-07-31}
	[score::10]
- [ ] (+) Social confidence and intimacy ([[Три основные цели на 2026]]) #MyGoals #MyGoals/2026 #MyGoals/2026/SocialConfidenceAndIntimacy @{2026-06-15} [score::10]


## 💚 Health & Self-Care [P::5]

- [ ] 🙂🎓 Have a course about Wellbeing at Coursera #Health/Resource #Health/Wellbeing [score::7] [time::2h] @{2026-06-06}
- [ ] 🛒 Buy an HRV (heart rate variability) monitoring bracelet for myself: Huawei Band 11/10 #Health/Physical #Tech #Buy @{2026-06-05} [score::14] [finance::3000] [time::45m]
- [ ] 🩺 Take PSA test in August #Health/Physical #Regular @{2026-08-16} [score::12] [time::120m] [finance::planned]
- [ ] 🧪 Take Invitro oncology markers + Vitamin D test #Health/Physical #Priority/High @{2026-07-15} [score::18] [time::45m] [finance::7000]
- [ ] 💡 Buy blue-spectrum light therapy glasses #Health/Physical #Health/Mental #Shopping/Technics @{2026-06-07} [score::11] [time::20m] [finance::5000]
- [ ] 🛠 Review: Implement to habits Mental and Physical Health ([[Три основные цели на 2026]])  #Habits  #Health/Physical #Health/Mental  @{2026-08-31} [score::12] [time::30m]
- [ ] 🏥 Make an X-ray shot #Health/Physical @{2026-06-04} [score::17] [time::15m] [finance::free]
- [ ] ⌚ Buy Garmin Venu smart watch #Health/Physical #Shopping/Technics @{2026-11-16} [score::14] [time::60m] [finance::45000]
- [ ] 🛠 Изучить повторно варианты [[HRV-браслетов (heart rate variability)]]. Подумать о второй покупке #Health/Physical #Health/Resource #Tech #Buy @{2026-09-01} [score::6] [finance::planned]
- [ ] 🩺 Check Welltory (free version) #Health/Resource #Digital/Tools @{2026-06-13} [score::9] [time::60m] [finance::free]
- [ ] ❗ Записаться на КТ ЛПС:
	- [Санкт-Петербург, м. Проспект Просвещения, проспект Энгельса, 138 корпус 1](https://domedica24.ru/contact/)
	- Время работы:**9:00 - 22:00**
	- [+7 (812) 380-83-84](tel:+78123808384)
	- Получить направление от Терапевта
	#Health/Physical #Priority/Highest  [score::15] [finance::free] @{2026-06-15}
- [ ] Go for an orthodontic consultation along with tooth control 17 #Health/Physical #Stomatology [category::Health] [score::12] @{2026-07-14}
- [ ] Make a lipidogram again (липидный профиль) - sign up to GP [score::15] [finance::free] #Health/Physical @{2026-09-01}
- [ ] 🩺 Visit endocrinologist — testosterone course (Смирнова Ирина Петровна, Бицоева Роксана Валерьевна) #Health/Physical #Health/Mental @{2026-06-10} [score::21] [time::30m] [finance::planned]


## 🏠🛒 Family, Home and Shopping  [P::5]

- [ ] 🟢 Vaccinate the cat Shiva #Subject/Cat #Cat #Family [score::15] @{2026-06-04} [time::1h30m]
- [ ] 🪟 Find and hang curtains on the balcony #Home #Decor @{2026-06-06} [score::9] [time::2h] [finance::free]
- [ ] 🐱 Put tick prevention collar on Shiva #Home #Pet/Shiva #Shopping @{2026-06-10} [score::5] [time::10m] [finance::extra]
- [ ] ❗Get apartment payments from tenants @{2026-06-04} #Regular  #Rent #Finance/Income [finance::income] [time::10min] [score::10]  [repeat:: every month on the 4th]  [scheduled:: 2026-06-04]
- [ ] 🟠 Check pension savings allocation in Alfa-Investments #Finance/Pension @{2026-08-05} [score::10] [time::30m] [finance::planned]
- [ ] ⏸ Enable GPB Premium subscription if salary is full; re-enable later (decision deadline: 05.06) #Finance/Banking @{2026-06-05} [score::13] [time::15m] [finance::regular]
- [ ] 🟢 Buy USB-flash or SATA drive to store all family photographs #Family #Buy #Home/Buying [score::7] [finance::planned] @{2026-06-20}
- [ ] 🔗 Buy a silver chain necklace #Shopping #Personal @{2026-06-07} [score::6] [time::30m] [finance::7000]


## 🚀 Enterprener & Career [P::5]

- [ ] 📝 Review clinic administrator’s meeting outcomes and materials @{2026-06-07} #Projects/AI-agents-employee [score::15] [time::120] [finance::income]
- [ ] 🎯 Pass the probationary period successfully #Career #SelfDevelopment @{2026-07-10} [score::23] [time::continuous] [finance::income]


## 🤖 AI and Dev [P::5]

- [ ] Изучить как работать с [gstack](https://github.com/garrytan/gstack) #Dev #AI/Agents [score::13] @{2026-06-23}
- [ ] Изучить [opencode](https://github.com/anomalyco/opencode) #Dev [score::15] @{2026-07-04}
- [ ] 🎓 Complete [[AI in corporate finance training course]] (15 lessons, one lesson per week) #Learning #AI/Learning #Project #Regular @{2026-06-05} [score::16] [time::1.5h] [finance::free]  [repeat:: every week on Thursday]  [scheduled:: 2026-05-28]
- [ ] ⏸  Pause: [[План действий по персональному ассистенту (KB)]]  @{2026-07-02} #TaskTracker/FocusFlow [score::10]  [priority:: low]  [repeat:: every day when done]  [start:: 2026-05-11]
- [<] ⏸ Pause: Lighthouse (Маяк) project ([[Общая информация по проекту]]) #Projects/Lighthouse[score::2] [finance::income] @{2026-09-01}
- [ ] 🛠 Next step on Local-AI-Dev-Platform Projects #Projects #Dev/AI #Projects/Local-AI-Dev-Platform #AI/Agents @{2026-06-13} [score::12]  [priority:: high]  [time::20m] [repeat:: every day when done]  [start:: 2026-03-25]
- [ ] 🟠 Explore the OpenClaw Agent System #AI/Agents #AI/Agents/OpenClaw  @{2026-06-04} [score::17] [time::120m]


## 🌟 Self-Dev and North-Star [P::5]

- [/] 🟢 [[Посмотреть видео TED Talk и ДНК Лидера|Watch TED Talk videos]] #SelfDevelopment  [score::7] #Regular  [time::30m][finance::free] @{2026-06-07}  [priority:: medium]  [repeat:: every day when done]  [start:: 2026-04-06]
- [ ] Work through every humiliation and negative self-identification ([[Мои унижения (убеждения)]]) #SelfReflection #SelfDevelopment [score::12] @{2026-06-09}
- [ ] 🛠 Test the state-control system workflow with ChatGPT #Projects #AI #Health/Resource #SystemsThinking @{2026-06-06} [score::18] [time::60m] [finance::free]
- [ ] 🔄 Next task in: [[План реализации целей из North Star (KB)]] #MyGoals #MyLifeGoals #Today  #Project   #Projects/NorthStar #MyGoals/NorthStar  [score::10] [time::30m] @{2026-06-08}  [repeat:: every day when done]  [scheduled:: 2026-04-05]
- [ ] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-06-07} [score::17]  [time::30m]  [repeat:: every week on Sunday]  [start:: 2026-06-07]
- [ ] Implement [[Протокол стабилизации самооценки]] #SelfDevelopment/SelfReflection [score::16] [finance::free] @{2026-08-04}
- [ ] 🟢 Implement habits: [[Привычки на фазу трансформации]] @{2026-07-13} #Habits #MyGoals/2026 [score::7] [time::60m]


## 🎸 Hobbies [P::4]

- [/] 🎵 Listen to music in the folder: M:\!I will play that staff\!Parties #Hobbies/DJing #Music/Preparation #Regular @{2026-06-06} [score::4] [finance::free] [time::1.5h]
- [ ] 🎤 Attend a vocal lesson #Hobbies/Vocal @{2026-06-08} [score::12] [time::4h] [finance::2500]  [repeat:: every week on Saturday]  [scheduled:: 2026-06-08]


## 🧩 Other Projects [P::3]

- [ ] 🚗 Research car options in Russia and Belarus #Personal #Finance/Planning #Shopping/Car @{2026-06-05} [score::8] [time::90m] [finance::planned]
- [ ] 🗑️ Take garbage to the recycling point (Зелёнка) #Home #Ecology @{2026-06-06} [score::8] [time::3h] [finance::extra] [cost::1200]
- [ ] 🏘️ Find an apartment to move to in Saint Petersburg #Home #Housing #Regular  @{2026-07-05} [score::22] [time::3h] [finance::planned]
- [ ] 🛠 Prepare second BI.Zone deliverable #Career #Projects/BIZone #Priority/Highest @{2026-06-05} [score::21] [time::4h] [finance::income] [tracking::external]
- [ ] 🏦 Switch GPB Premium to a different plan — check options with support #Finance/Banking @{2026-06-05} [score::13] [time::30m] [finance::regular]
- [ ] 💡 If financial losses occur — compensate the shortfall from regular savings to pension savings. Earn should be no less than 10% #Finance/Strategy #Personal @{2026-09-15} [score::10] [time::30m] [finance::planned]
- [ ] 💡 [[ИИ озвучка книг как проект|AI audiobook dubbing as a project]] — explore as a potential income stream #Projects #Hobbies/Dubbing #AI @{2026-07-01} [score::9] [finance::maybe]
- [ ] ❗Check cryptocurrency courses from Misha from Cheboksary #Cryptocurrency #Learning/Crypto [score::17] [time::20h] @{2026-06-05}


## ⏳ BACKLOG



## 🏁 DONE

- [x] 🖼 Post Skazka's poster to chanell and vK #MyGoals/2026/SkazkaFestival @{2026-05-31} [score::7] [time::30m]  [completion:: 2026-05-31]
- [x] Cleen the flat #Hygiene [score::12]  [completion:: 2026-05-31]
- [x] 🍬 Order a sweetener #Health/Nutrition #Regular @{2026-05-30} [score::17] [time::10m] [finance::planned] [cost::1000]  [completion:: 2026-05-30]
- [x] 🟠 Read my Goals: [[Три основные цели на 2026]]  #MyGoals/2026 #Regular @{2026-05-29} [score::8]  [repeat:: every week when done]  [start:: 2026-05-29]  [completion:: 2026-05-29]
- [x] 💊 Research statins and cardiovascular prevention strategy  [[Работа с липидами и липидограмма (план снижения риска инфаркта)]] #Health/Research #Priority/Highest @{2026-05-29} [score::16] [time::90m] [finance::free]  [completion:: 2026-05-29]
- [x] 🚭 Start day 3 of not smoking ([[Памятка курильщику]]) #SelfDevelopment #Health/Physical @{2026-05-28} [score::23]  [due:: 2026-05-26]  [completion:: 2026-05-29]
- [x] 📁 Fill in the files in the Systems folder in Obsidian #Tasks/Admin #Obsidian #SelfDevelopment @{2026-05-25} [score::17] [time::45m] [finance::free]  [completion:: 2026-05-28]
- [x] 🎤 Attend a vocal lesson #Hobbies/Vocal @{2026-05-28} [score::12] [time::2h] [finance::2500]  [repeat:: every week on Saturday]  [scheduled:: 2026-05-28]  [completion:: 2026-05-28]
- [x] 👟 Get sneakers repaired: [  [completion:: 2026-05-28]
	ул. Маршала Тухачевского, 13](https://yandex.ru/profile/213231662288?lang=ru)  #Home #Personal #Shopping @{2026-05-27} [score::8] [time::30m] [finance::1500]
- [x] 💊 Buy Omega-3-6-9 @{2026-05-27} #Health/Physical [score::12]  [completion:: 2026-05-28]
- [x] 🚭 Start day 2 of not smoking ([[Памятка курильщику]]) #SelfDevelopment #Health/Physical @{2026-05-27} [score::23]  [due:: 2026-05-26]  [completion:: 2026-05-28]
- [x] 🎪 Send Skazka Festival follow-up message to Sonic #MyGoals/2026/SkazkaFestival #Networking @{2026-05-27} [score::12] [time::15m] [finance::free]  [completion:: 2026-05-27]
- [x] 🚭 Start day 1 of not smoking ([[Памятка курильщику]]) #SelfDevelopment #Health/Physical @{2026-05-26} [score::23]  [due:: 2026-05-26]  [completion:: 2026-05-27]
- [x] 🔪 Buy a knife sharpener #Home #Kitchen #Shopping @{2026-05-25} [score::7] [time::15m] [finance::300]  [completion:: 2026-05-25]
- [x] 🥫 Buy a can opener #Home #Kitchen #Shopping @{2026-05-25} [score::5] [time::15m] [finance::500]  [completion:: 2026-05-25]
- [x] ❗Prepare to health checkup:  [completion:: 2026-05-24]
	- [x] Проверить предыдущие анализы на состав онкомаркеров: ПСА, ЖКТ  [completion:: 2026-05-24]
	- [x] Проговорить с ChatGPT на предмет анализов: [[Какие анализы на онкомаркеры рекомендуется сдавать мужчине после 45 лет]]  [completion:: 2026-05-24]
	- [x] Дождаться теста Генотек  [completion:: 2025-12-24]
	#Health/Physical #Priority/Highest  [score::20] [finance::planned] @{2026-05-24}
- [x] 🔄 Move recurring weekly/monthly tasks to a reminder app (Reminders or Calendar) #Tasks/Admin #Kanban @{2026-05-24} [score::14] [time::30m] [finance::free]  [completion:: 2026-05-24]
- [x] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-05-24} [score::17]  [time::30m]  [repeat:: every week on Sunday]  [start:: 2026-05-24]  [completion:: 2026-05-24]
- [-] 🟠 Await: Modify summary bot #Dev/Bots #Dev/Bots/StructDevSummaryBot [score::9] [finance::free] [time::120min] @{2026-05-12}  [cancelled:: 2026-05-12]
- [x] Make a lipidogram again (липидный профиль) - sign up to GP [score::15] [finance::free] #Health/Physical @{2026-05-25}  [completion:: 2026-05-25]
- [x] Talk to GP:  [completion:: 2026-05-25]
	- Lipidogram
	- [[Какие анализы на онкомаркеры рекомендуется сдавать мужчине после 45 лет]]
	- [[Brain-Boosting Supplements]]
	[score::15] [finance::free] #Health/Physical @{2026-05-25}
- [x] 🟢 Watch the Otus webinar on Interaction with stakeholders #Learning/Otus [score::11] [finance::free] @{2026-05-26}  [completion:: 2026-05-26]
- [x] 🖼 Ask Toni to send me a Skazka's poster #MyGoals/2026/SkazkaFestival @{2026-05-27}  [completion:: 2026-05-27]
- [x] 🐾 Order pet food #Home/Pets #Regular @{2026-05-30} [score::12] [time::10m] [finance::regular] [cost::1500]  [completion:: 2026-05-30]
- [x] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-05-31} [score::17]  [time::30m]  [repeat:: every week on Sunday]  [start:: 2026-05-31]  [completion:: 2026-05-31]
- [x] 🌾 Buy ground flaxseed (лён) #Health/Nutrition #Shopping @{2026-06-01} [score::9] [time::15m] [cost::300]  [completion:: 2026-06-01]
- [x] Купить низкокалорийные леденцы, например, Sula [score::12] #Health/Physical @{2026-06-01}  [completion:: 2026-06-01]
- [x] 🏥 Sign up for a surgeon consultation #Health/Physical @{2026-06-01} [score::17] [time::15m] [finance::free]  [completion:: 2026-06-01]
- [x] 🌿 Buy psyllium husk (снижает холестерин) #Health/Nutrition #Shopping @{2026-06-01} [score::17] [time::15m] [cost::500]  [completion:: 2026-06-01]


***

## Archive

- [x] 📄 Discuss [[Вопросы по трудовому договору]] #Career #Legal @{2026-04-21} [score::25] [time::30m]  [completion:: 2026-04-22]  ||  2026-04-22 08:28
- [x] 💳 Pay Yandex 360 subscription #Finance/Subscriptions #Regular @{2026-04-21} [score::11] [time::5m] [finance::regular]  [completion:: 2026-04-21]  ||  2026-04-22 08:28
- [x] 🟢 Meet with Tima  and present him the gift #Family #Buy #Home/Buying @{2026-04-20}[score::21]  [completion:: 2026-04-20]  ||  2026-04-22 08:28
- [x] 🛤 Buy train ticket for Lyuba #Family/Buying #Family/Liubov @{2026-04-19} [score::20] [time::10m] [finance::planned]  [completion:: 2026-04-20]  ||  2026-04-22 08:28
- [x] 📦 Send jacket from Saint Petersburg to Moscow #Family #Home @{2026-04-20} [score::16] [time::20m] [finance::free]  [completion:: 2026-04-20]  ||  2026-04-22 08:28
- [x] 🤝 Contact Dina #Social #Networking @{2026-04-19} [score::13] [time::15m]  [completion:: 2026-04-20]  ||  2026-04-22 08:28
- [x] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-04-19} [score::17]  [repeat:: every week on Sunday]  [start:: 2026-03-29]  [completion:: 2026-04-20]  ||  2026-04-22 08:28
- [x] 💊 Get new prescripts from Gorbatsevich @{2026-04-19} #Health/Mental [score::21]  [completion:: 2026-04-19]  ||  2026-04-22 08:28
- [x] 🟠 Sort out tasks on Kanban in interval from 11 to 15 #Tasks/Admin #Kanban [score::10] @{2026-04-19}  [completion:: 2026-04-19]  ||  2026-04-22 08:28
- [x] 💰 Collect money for Anton's kilt gift (birthday present) #Family #Social @{2026-04-23} [score::19] [time::10m] [finance::extra]  [completion:: 2026-04-27]  ||  2026-05-03 05:44
- [x] Купить таблетки:  [completion:: 2026-04-27]
	- [x] Золофт  [completion:: 2026-04-27]
	- [x] Ламотриджин  [completion:: 2026-04-27]
	@{2026-04-26}  ||  2026-05-03 05:44
- [x] 🏗️ Find a geodesic engineer for father's land project #Projects/FathersLand #Family @{2026-04-24} [score::14] [time::30m] [finance::planned]  [completion:: 2026-04-27]  ||  2026-05-03 05:44
- [x] Выложить посты про Сказку в разных сетях @{2026-04-23}  [completion:: 2026-04-27]  ||  2026-05-03 05:44
- [x] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-04-22}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-04-22]  [completion:: 2026-04-23]  ||  2026-05-03 05:44
- [x] 🟢 Meet with Tima  and present him the gift #Family #Buy #Home/Buying @{2026-04-22}[score::21]  [completion:: 2026-04-23]  ||  2026-05-03 05:44
- [x] 🔄 Make Pilling with Exosomes #Regular #Cosmetology #Health/Physical @{2026-05-06} [score::16] [finance::free]  [repeat:: every week when done]  [scheduled:: 2025-11-24]  [completion:: 2026-05-07]  ||  2026-05-08 13:41
- [x] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-05-06}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-05-06]  [completion:: 2026-05-06]  ||  2026-05-08 13:41
- [x] 🎓 Get AI course access from Dima #Learning #AI/Learning @{2026-05-05} [score::14] [time::15m] [finance::free]  [completion:: 2026-05-06]  ||  2026-05-08 13:41
- [x] 🚿 Buy shower gel #Hygiene #Shopping @{2026-05-05} [score::9] [time::10m] [finance::extra]  [completion:: 2026-05-06]  ||  2026-05-08 13:41
- [x] ❗Check receipt of apartment payments from tenants @{2026-05-05} #Regular  #Rent #Finance/Income [finance::income] [time::10min] [score::10]  [repeat:: every month on the 4th]  [scheduled:: 2026-07-04]  [completion:: 2026-05-06]  ||  2026-05-08 13:41
- [x] Unpack clothes and staff after the trip [score::14] @{2026-05-05}  [completion:: 2026-05-06]  ||  2026-05-08 13:41
- [x] ⏸ Disable GPB Premium subscription if salary is not full; re-enable later (decision deadline: 07.05) #Finance/Banking @{2026-05-05} [score::13] [time::15m] [finance::regular]  [completion:: 2026-05-05]  ||  2026-05-08 13:41
- [x] 🚂 Move to St. Petersburg — pack things, evening train @{2026-05-03} [score::20] [time::180m] [finance::planned]  [completion:: 2026-05-04]  ||  2026-05-08 13:41
- [x] 👵 Visit aunt Ira and give her the gifts @{2026-05-03} [score::15] [time::120m] [finance::free]  [completion:: 2026-05-04]  ||  2026-05-08 13:41
- [x] 📱 Free SIM card — decide what to do with it #Tech/Support #Personal @{2026-04-29} [score::6] [time::20m] [finance::free]  [completion:: 2026-05-03]  ||  2026-05-08 13:41
- [x] 💰 Get rent money from father for the apartment #Family/Finances #Finance @{2026-04-28} [score::16] [time::10m] [finance::income]  [completion:: 2026-05-03]  ||  2026-05-08 13:41
- [x] 🟠 Read my Goals: [[Три основные цели на 2026]]  #MyGoals/2026 @{2026-04-28} [score::5]  [repeat:: every week when done]  [start:: 2026-04-26]  [completion:: 2026-05-03]  ||  2026-05-08 13:41
- [x] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-04-29}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-04-29]  [completion:: 2026-05-03]  ||  2026-05-08 13:41
- [x] 🟢 To pay Tinkoff credit card debt #Regular  #Finance/Debts @{2026-05-06}  [score::10] [finance::debts]  [repeat:: every month on the 6th]  [scheduled:: 2026-05-06]  [completion:: 2026-05-06]  ||  2026-05-08 13:41
- [x] 🟢 To pay Tinkoff credit card debt #Regular  #Finance/Debts @{2026-05-06}  [score::10] [finance::debts]  [repeat:: every month on the 6th]  [scheduled:: 2026-06-06]  [completion:: 2026-05-07]  ||  2026-05-08 13:41
- [x] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-05-06}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-05-13]  [completion:: 2026-05-07]  ||  2026-05-08 13:41
- [x] 🪒 Shave the lower body #Hygiene #Personal @{2026-05-07} [score::9] [time::15m] [finance::free]  [completion:: 2026-05-07]  ||  2026-05-08 13:41
- [x] 🔊 Set up Yandex Alice smart speaker #Home #Tech/Setup @{2026-05-09} [score::9] [time::20m] [finance::free]  [completion:: 2026-05-10]  ||  2026-05-11 15:00
- [x] 📦 Unpack the delivery from CDEK #Home #Shopping @{2026-05-09} [score::12] [time::30m] [finance::free]  [completion:: 2026-05-10]  ||  2026-05-11 15:00
- [x] 💊 Order vitamin C for myself #Health/Physical #Shopping @{2026-05-09} [score::8] [time::10m] [finance::extra]  [completion:: 2026-05-08]  ||  2026-05-11 15:00
- [x] 📦 Get the delivery from CDEK #Home #Shopping @{2026-05-08} [score::17] [time::30m] [finance::free]  [completion:: 2026-05-08]  ||  2026-05-11 15:00
- [x] ✉️ Write to Sonic about slots at Skazka Festival #Hobbies/DJing #Social #Networking @{2026-05-11} [score::19] [time::10m] [finance::free]  [completion:: 2026-05-11]  ||  2026-05-11 20:41
- [x] 🧹 Do a cleaning of the apartment #Home #Regular @{2026-05-11} [score::20] [time::90m] [finance::free]  [completion:: 2026-05-11]  ||  2026-05-11 20:41
- [x] 🎛 Prepare Promomix for Skazka Festival #Hobbies/DJing #Music/Preparation @{2026-05-11} [score::21] [finance::free] [time::180min]  [completion:: 2026-05-11]  ||  2026-05-11 20:41
- [x] 🛠 Изучить варианты [[HRV-браслетов (heart rate variability)]]  (Whoop / Garmin / Polar H10) — выбрать модель, занести в вишлист #Health/Physical #Health/Resource #Tech #Buy @{2026-05-16} [score::15] [finance::planned]  [completion:: 2026-05-17]  ||  2026-05-17 13:14
- [x] 📱 Find a button/flip phone for father #Family #Shopping @{2026-05-16} [score::10] [time::30m] [finance::planned]  [completion:: 2026-05-16]  ||  2026-05-17 13:14
- [x] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-05-15}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-05-20]  [completion:: 2026-05-15]  ||  2026-05-17 13:14
- [x] 📋 Compile a list of requests for the GP visit: endocrinologist, CT shoulder, MRI of the lower spine, lipidogram, left kneel, общая усталость и постоянный сон #Health #Health/Planning @{2026-05-15} [score::17] [time::30m] [finance::free]  [completion:: 2026-05-15]  ||  2026-05-17 13:14
- [x] 🐱 Order tick prevention for the cat: drops and collar #Home #Pet/Shiva #Shopping @{2026-05-14} [score::11] [time::10m] [finance::extra]  [completion:: 2026-05-15]  ||  2026-05-17 13:14
- [x] 💡 Buy new Kojima E14-RGB light bulbs (x2) #Home #Shopping @{2026-05-14} [score::7] [time::10m] [finance::extra]  [completion:: 2026-05-15]  ||  2026-05-17 13:14
- [x] 🟠 Read my Goals: [[Три основные цели на 2026]]  #MyGoals/2026 @{2026-05-14} [score::8]  [repeat:: every week when done]  [start:: 2026-05-10]  [completion:: 2026-05-15]  ||  2026-05-17 13:14
- [x] 🟠  Make a [[Monthly report on family expenses]] #Regular #Finance/Reports #Family #Family/Finances #Priority/Highest @{2026-05-12} [finance::free] [score::9]  [time::90m]  [priority:: highest]  [repeat:: every month]  [scheduled:: 2026-05-01]  [completion:: 2026-05-14]  ||  2026-05-17 13:14
- [x] 🧠 Make an appointment with a psychologist #Health/Mental #SelfDevelopment @{2026-05-12} [score::21] [finance::planned]  [completion:: 2026-05-14]  ||  2026-05-17 13:14
- [x] Купить [score::12]:  [completion:: 2026-05-12]
	- [x] Кофе в зёрнах  [completion:: 2026-05-07]
	- [x] Жидкость для стирки цветного белья @{2026-05-11}  [completion:: 2026-05-07]  ||  2026-05-17 13:14
- [x] 🥗 Prepare a personal diet plan using ChatGPT and Claude #Health/Physical #SelfDevelopment @{2026-05-11} [score::14] [time::60m] [finance::free]  [completion:: 2026-05-12]  ||  2026-05-17 13:14
- [x] 💡 Set up LED light strip via smart socket #Home #Tech/Setup @{2026-05-11} [score::7] [time::20m] [finance::free]  [completion:: 2026-05-11]  ||  2026-05-17 13:14
- [x] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-05-11} [score::17]  [repeat:: every week on Sunday]  [start:: 2026-04-05]  [completion:: 2026-05-11]  ||  2026-05-17 13:14
- [x] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-05-11} [score::17]  [repeat:: every week on Sunday]  [start:: 2026-04-12]  [completion:: 2026-05-12]  ||  2026-05-17 13:14
- [ ] 🏠 Resolve tenant registration issue for the apartment #Home #Legal #Rent @{2026-05-20} [score::4] [time::30m] [finance::free]  ||  2026-05-17 13:44
- [x] 📖 Re-read the article about evolution of agents ([link](https://t.me/Struct_dev/1/720)) #AI/Agents @{2026-05-23} [score::5] [time::7m] [finance::free]  [completion:: 2026-05-24]  ||  2026-05-24 13:32
- [x] 🎤 Attend a vocal lesson #Hobbies/Vocal @{2026-05-23} [score::12] [time::2h] [finance::2500]  [repeat:: every week on Saturday]  [scheduled:: 2026-05-23]  [completion:: 2026-05-24]  ||  2026-05-24 13:32
- [x] 🟢 Understand how to use AI in work and everyday activities #MyGoals/2026   ([[Другие цели и планы на 2026 год]]) [score::13] [finance::free] @{2026-05-23}  [completion:: 2026-05-24]  ||  2026-05-24 13:32
- [x] 🔌 Buy HDMI cable (3 or 5 meters) #Home #Tech/Setup #Shopping @{2026-05-22} [score::8] [time::15m] [finance::1500]  [completion:: 2026-05-22]  ||  2026-05-24 13:32
- [x] 📃 Create [wishlist](https://ohmywishes.com/users/jbitch) for myself #Personal #SelfCare #Family @{2026-05-21} [score::7] [finance::to_plan] [time::1h]  [completion:: 2026-05-21]  ||  2026-05-24 13:32
- [x] 🎓 Complete AI in corporate finance training course (15 lessons, one lesson per week) #Learning #AI/Learning #Project #Regular @{2026-05-21} [score::16] [time::1.5h] [finance::free]  [repeat:: every week on Thursday]  [scheduled:: 2026-05-21]  [completion:: 2026-05-21]  ||  2026-05-24 13:32
- [x] 💈 Get a haircut #Hygiene #Personal @{2026-05-20} [score::6] [time::60m] [finance::1600]  [completion:: 2026-05-20]  ||  2026-05-24 13:32
- [x] 💳 Buy a card holder for bank cards #Buy #Personal #Home @{2026-05-20} [score::7] [time::15m] [finance::extra]  [completion:: 2026-05-20]  ||  2026-05-24 13:32
- [x] 🧴 Order face creams through Lyuba #Home #SelfCare #Shopping @{2026-05-20} [score::9] [time::10m] [finance::extra]  [completion:: 2026-05-20]  ||  2026-05-24 13:32
- [x] 🍳 Buy frying pans #Home #Cooking #Shopping @{2026-05-20} [score::9] [time::30m] [finance::4000]  [completion:: 2026-05-20]  ||  2026-05-24 13:32
- [x] 🛏️ Buy bed sheets #Home #Shopping @{2026-05-21} [score::9] [time::20m] [finance::500]  [completion:: 2026-05-20]  ||  2026-05-24 13:32
- [x] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-05-20}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-06-03]  [completion:: 2026-05-20]  ||  2026-05-24 13:32
- [x] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-05-20}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-05-27]  [completion:: 2026-05-20]  ||  2026-05-24 13:32
- [x] 💊 Buy Aripiprazole #Health/Mental #Shopping @{2026-05-19} [score::16] [time::30m] [finance::5000]  [completion:: 2026-05-19]  ||  2026-05-24 13:32
- [x] 🔴 Pay communal bills for flat in SPB #Home #Finance/Utilities #Regular @{2026-05-19} [score::6]  [priority:: high]  [repeat:: every month]  [scheduled:: 2026-04-15]  [completion:: 2026-05-19]  ||  2026-05-24 13:32
- [x] ❗ Get paper certificate from Otus ([Check-list](https://drive.google.com/file/d/1Nn68vUo9syRHWqNHgU2JLyFw5lMKfrDo/view?usp=sharing)) #Learning/Otus    [score::17] [finance::free] [time::30m] @{2026-05-18}  [completion:: 2026-05-18]  ||  2026-05-24 13:32
- [x] 🔄 Make Pilling with Exosomes #Regular #Cosmetology #Health/Physical @{2026-05-17} [score::6] [finance::free]  [repeat:: every week when done]  [scheduled:: 2026-05-14]  [completion:: 2026-05-18]  ||  2026-05-24 13:32
- [x] 🧹 Do a clean of the apartment #Home #Regular #Hygiene @{2026-05-17} [score::9] [time::90m] [finance::free]  [completion:: 2026-05-17]  ||  2026-05-24 13:32
- [x] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-05-17} [score::17]  [repeat:: every week on Sunday]  [start:: 2026-04-19]  [completion:: 2026-05-17]  ||  2026-05-24 13:32
- [x] 🔄 Weekly priority review: check and rebalance score intervals every Sunday #Tasks/Admin #Kanban #Regular @{2026-05-17} [score::17]  [repeat:: every week on Sunday]  [start:: 2026-04-26]  [completion:: 2026-05-18]  ||  2026-05-24 13:32
- [x] 🟠 Read my Goals: [[Три основные цели на 2026]]  #MyGoals/2026 @{2026-05-22} [score::8]  [repeat:: every week when done]  [start:: 2026-05-22]  [completion:: 2026-05-22]  ||  2026-05-24 13:32
- [x] 📊 First deliverable for Rostislav #Career #Projects/Rostislav @{2026-05-22} [score::21] [time::120m] [finance::income]  [completion:: 2026-05-22]  ||  2026-05-24 13:32
- [ ] 🔄 Make Pilling with Exosomes #Regular #Cosmetology #Health/Physical @{2026-05-27} [score::6] [finance::free]  [repeat:: every week when done]  [scheduled:: 2026-05-25]  ||  2026-05-24 13:59
- [ ] 🟢 To pay Tinkoff credit card debt #Regular  #Finance/Debts @{2026-06-06}  [score::7] [finance::debts]  [repeat:: every month on the 6th]  [scheduled:: 2026-06-06]  ||  2026-05-24 14:01
- [ ] 🟢 Прочитать [[North Star (12–15 месяцев)]] #MyGoals #MyGoals/NorthStar #MyLifeGoals #Regular  [score::17] [time::10m] @{2026-05-27}  [priority:: high]  [repeat:: every week on Wednesday]  [due:: 2026-05-27]  ||  2026-05-24 14:15
- [ ] 💍 Buy Oura Ring 4 #Health/Physical #Shopping/Technics @{2026-09-01} [score::6] [time::45m] [finance::45000]  ||  2026-05-26 12:39
- [ ] 🔄 Build a weekly review system for state map course [ChatGPT::Карта состояния через три месяца] #SelfDevelopment #Learning @{2026-05-31} [score::15] [time::45m] [finance::free]  ||  2026-05-31 16:40
- [ ] 📸 Post Instagram video: how I play my DJ set  (all versions + links to SC and vK):
	- Videos i can find from 21.02 
	#Hobbies/DJing #SocialMedia #Marketing  #Regular  
	@{2026-05-31} [score::8] [finance::free] [time::30min]  [repeat:: every day when done]  [start:: 2026-04-04]  ||  2026-05-31 21:04

%% kanban:settings
```
{"kanban-plugin":"board","show-checkboxes":true,"full-list-lane-width":true,"move-tags":true,"tag-action":"kanban","tag-colors":[{"tagKey":"#Priority/High","color":"rgba(250, 137, 137, 1)","backgroundColor":""},{"tagKey":"#Priority/Highest","color":"rgba(255, 2, 2, 1)","backgroundColor":"rgba(151, 38, 189, 0.38)"},{"tagKey":"#DelegatedBef","color":"rgba(255, 250, 210, 1)","backgroundColor":""},{"tagKey":"#ToDelegate","color":"rgba(215, 221, 80, 1)","backgroundColor":"rgba(126, 126, 126, 0.1)"},{"tagKey":"#Delegated","color":"rgba(255, 255, 255, 1)","backgroundColor":"rgba(255, 227, 71, 0.62)"},{"tagKey":"#Regular","color":"rgba(196, 197, 80, 1)","backgroundColor":"rgba(26, 26, 26, 0.1)"},{"tagKey":"#Project","color":"rgba(0, 231, 8, 1)","backgroundColor":"rgba(84, 199, 0, 0.07)"},{"tagKey":"#Today","color":"rgba(231, 107, 107, 1)","backgroundColor":"rgba(245, 116, 93, 0.1)"}],"move-dates":true,"show-relative-date":true,"archive-with-date":true,"append-archive-date":true,"date-picker-week-start":1,"move-task-metadata":true,"metadata-keys":[],"inline-metadata-position":"footer","list-collapse":[true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false],"lane-width":350,"table-sizing":{"date":150},"archive-date-separator":" || "}
```
%%