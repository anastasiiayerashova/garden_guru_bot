# 🌿 GardenGuru — AI Plant Expert Bot

**GardenGuru** — це інтелектуальний Telegram-бот, розроблений для допомоги садівникам, фермерам та любителям кімнатних рослин. Бот поєднує в собі потужність комп'ютерного зору та штучного інтелекту для розпізнавання флори, точної діагностики хвороб та надання персоналізованих агрономічних порад. Проєкт використовує агентну архітектуру ReAct (Reason + Act), що дозволяє моделі самостійно приймати рішення про використання інструментів для вирішення завдань користувача.

---

## 🚀 Основні можливості

- **📸 Фото-ідентифікація:** Миттєве визначення виду рослини за фотографією за допомогою **Pl@ntNet API** (база з понад 45,000 видів).
- **🏥 Діагностика хвороб:** Спеціалізований аналіз симптомів (плями, наліт, шкідники) через ендпоїнт `/diseases/identify`.
- **🤖 AI Консультант:** Використання **OpenAI GPT-5.4-nano** для синтезу відповідей на основі візуальних даних та експертної бази знань.
- **🧮 Садовий калькулятор:** Розрахунок площі ділянок, норм внесення добрив та об'ємів поливу безпосередньо у чаті.
- **📖 Semantic Search:** Розумний пошук по внутрішній базі знань GardenGuru для надання точних інструкцій з догляду.
- **📅 Агро-календар:** Рекомендації щодо оптимальних термінів посадки та проведення робіт.

---

## 📂 Структура проєкту

Проєкт організований за модульним принципом, що забезпечує чіткий розподіл відповідальності між компонентами:

### ⚡ (Ядро системи)

- **`main.py`** — Точка входу. Ініціалізує Telegram-бота, реєструє роутери та запускає асинхронне опитування (Polling).
- **`handlers.py`** — Модуль обробки повідомлень. Містить логіку реагування на команди (`/start`, `/identify`, `/disease`) та вхідні медіафайли.
- **`init.py`** — Налаштування LangGraph, моделі та MemorySaver.

### 🧠 AI та Vision

- **`vision_services.py`** — Модуль інтеграції з **Pl@ntNet API**. Відповідає за HTTP-запити для ідентифікації видів рослин та патологій за допомогою комп'ютерного зору.
- **`services.py`** — Взаємодія з **OpenAI API**. Керує контекстом діалогу та логікою "мислення" Агента GPT-5.4-nano.
- **`tools.py`** — Набір інструментів (Functions), які Агент може викликати самостійно: пошук по базі, калькулятори та специфічні садові розрахунки.

### 🛠 Допоміжні модулі (Utilities)

- **`utils.py`** — Центр конфігурації бота.
- **`schemas.py`** — Визначення структур даних за допомогою **Pydantic**. Гарантує, що відповіді від API та вхідні дані відповідають очікуваному формату.
- **`logger_config.py`** — Налаштування формату логів та рівнів відстеження помилок для стабільної роботи 24/7.
- **`test_bot.py`** — Модуль для автоматизованого тестування. Дозволяє імітувати запити користувачів та перевіряти коректність роботи логіки без ручного запуску бота.

### 📦 Дані та конфігурація

- **`knowledge_db.txt`** — Локальна база знань у текстовому форматі, яка використовується для семантичного пошуку (RAG).
- **`.env`** — Файл з чутливими даними (токени, ключі API), який не потрапляє в репозиторій.
- **`.gitignore`** — Список файлів та папок, які ігноруються системою Git.

---

## 🛠 Технологічний стек

- **Python 3.10+**
- **Framework:** [aiogram 3.x](https://docs.aiogram.dev/) (Asynchronous framework)
- **Computer Vision:** [Pl@ntNet API](https://my.plantnet.org/)
- **LangGraph** (від LangChain) — для керування станами та циклами агента.
- **OpenAI API** — ядро штучного інтелекту.
- **LLM:** OpenAI API (`gpt-5.4-nano`)
- **Networking:** `aiohttp` (Asynchronous HTTP Client)
- **Pydantic** — для валідації аргументів інструментів.
- **Colorlog** — для візуально зрозумілої розробки та дебагу.

---

## 💻 Як запустити

1.  **Клонування репозиторію:**

    ```bash
    git clone https://github.com/anastasiiayerashova/garden_guru_bot.git
    ```

2.  **Встановлення залежностей:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Налаштування середовища:**
    Створіть файл .env у кореневій директорії та додайте ваші ключі. **Важливо:** кожна копія бота потребує власної бази знань в OpenAI.

    ```bash
    TELEGRAM_TOKEN=your_telegram_bot_token
    OPENAI_API_KEY=your_openai_api_key
    PLANTNET_API_KEY=your_plantnet_api_key
    # ID вашої бази знань (Vector Store), створеної на платформі OpenAI
    VECTOR_STORE_ID=your_vector_store_id
    MODEL_NAME=your_model_name
    TEMPERATURE=your_temperature
    ```

4.  **Запуск бота:**
    ```bash
    python src/main.py
    ```

---

## 📱 Telegram Bot

Проєкт реалізований як повноцінний асинхронний Telegram-бот, що поєднує можливості штучного інтелекту та комп'ютерного зору:

- **🧠 Розумні діалоги:** Використання `thread_id` дозволяє боту зберігати контекст тривалих розмов з кожним користувачем окремо.
- **👁️ Computer Vision:** \* **Ідентифікація:** Миттєве визначення виду рослини за фото.
  - **Діагностика:** Аналіз уражених ділянок для виявлення хвороб та шкідників.
- **📚 Retrieval-Augmented Generation (RAG):** Бот інтегрує дані з персоналізованої бази знань у відповіді GPT-5.4-nano, що гарантує точність порад.
- **🛡️ Безпека:** Автоматичні застереження про засоби захисту при згадці агрохімікатів та фільтрація нецільових запитів.

---

graph TD
%% Define Nodes (Elements)
Start((🆕 Користувач)) -->|Надсилає повідомлення| InputMsg[Отримання запиту в Aiogram]

    %% Router Logic
    InputMsg -->|Аналіз типу повідомлення| Router{Router / handlers.py}

    %% Branch 1: Commands
    Router -->|Команда /start, /help, /calc| SimpleResp[Відправка готового тексту]
    SimpleResp --> EndOutput

    %% Branch 2: Photo (Vision)
    Router -->|Фото рослини| VisionFlow[Завантаження фото]
    VisionFlow --> PlantNetPlant[Pl@ntNet API: Визначення виду]
    PlantNetPlant --> PlantNetDisease[Pl@ntNet API: Діагностика хвороби]
    PlantNetDisease --> PrepareAgentPrompt[Формування контексту для Агента]
    PrepareAgentPrompt --> AgentNode

    %% Branch 3: Text Request (LLM)
    Router -->|Текстове питання| AgentNode

    %% LLM Core Logic (ReAct Chain via LangGraph)
    subgraph AI_AGENT [🧠 Ядро Агента (GPT-5.4-nano)]
        AgentNode[Аналіз запиту] -->|Мислить: Які інструменти потрібні?| ToolSelection{Вибір Інструменту}
    end

    %% Tools Interaction
    ToolSelection -->|Потрібен RAG / знання| SemanticSearch[Semantic Search / Vector Store]
    ToolSelection -->|Потрібні розрахунки| CalcTool[Садовий Калькулятор]
    ToolSelection -->|Власні знання / Не по темі| GenerateResp[Формування фінальної відповіді]

    %% Back to Agent
    SemanticSearch -->|Отримано знання| AgentNode
    CalcTool -->|Результат розрахунку| AgentNode
    GenerateResp -->|Готова відповідь| OutputMsg[Асинхронна відповідь Aiogram]

    %% Final Outputs
    OutputMsg --> EndOutput((📤 Відповідь в Telegram))

    %% Styling (Optional but looks nice)
    style Router fill:#f96,stroke:#333,stroke-width:2px,color:white
    style ToolSelection fill:#f96,stroke:#333,stroke-width:2px,color:white
    style AI_AGENT fill:#e1f5fe,stroke:#01579b,stroke-width:1px
    style SemanticSearch fill:#fff3e0,stroke:#ff9800
    style CalcTool fill:#fff3e0,stroke:#ff9800
    style PlantNetPlant fill:#e8f5e9,stroke:#4caf50
    style PlantNetDisease fill:#e8f5e9,stroke:#4caf50

---

## 🛠 Обробка помилок та логування

У проєкті реалізована багаторівнева система відстеження подій:

- **Зелений (INFO)**: Повідомлення про успішні операції та запуск.
- **Жовтий (WARNING)**: Попередження про порожні відповіді або дивну поведінку.
- **Червоний (ERROR)**: Детальні стеки помилок (tracebacks) у разі збоїв у логіці чи API.

---

_Розроблено як сучасне рішення для автоматизації знань у сфері садівництва_

---

## 👩‍💻 About the Developer

**Anastasiia Yerashova** — Junior Full-Stack Developer passionate about writing clean and efficient code, growing professionally, and collaborating with purpose-driven teams.

> "As a passionate Junior Full-Stack Developer, I excel at delivering clean, reliable, and efficient solutions.  
> My goal is to grow professionally, achieve meaningful results, and work with people who share my drive for success.  
> I approach every task with responsibility and dedication, always giving 100%.  
> My ability to quickly adapt to new challenges and technologies allows me to thrive in agile and fast-paced environments."

## 📫 Contact

- [LinkedIn](www.linkedin.com/in/anastasia-yerashova)
- [GitHub](https://github.com/anastasiiayerashova)
- Email: yerashova.a@gmail.com

> Thank you for checking out the project! If you found it helpful or interesting, feel free to leave a ⭐ on the repository.
