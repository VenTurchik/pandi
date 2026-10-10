# Pandi

Эмулятор командной оболочки UNIX-подобной ОС.

**Учебный проект по дисциплине «Конфигурационное управление». Вариант №12.**

## Содержание

- [Общее описание](#общее-описание)
- [Установка и запуск](#установка-и-запуск)
- [Этап 1. REPL](#этап-1-repl)
- [Этап 2. Конфигурация](#этап-2-конфигурация)
- [Этап 3. VFS](#этап-3-vfs-виртуальная-файловая-система)
- [Этап 4. Основные команды](#этап-4-основные-команды)
- [Тесты](#тесты)

## Общее описание

`pandi` — консольный эмулятор командной оболочки, имитирующий работу
в UNIX-подобной ОС.

Все этапы фиксируются в истории коммитов репозитория.

## Установка и запуск

Требования:

- Python 3.10+
- pytest (для запуска тестов)

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Запуск эмулятора:
```bash
./run.sh
```

Запуск тестов(из корня репозитория)
```bash
pytest -v
```

## Этап 1. REPL
Что реализовано:
1. Консольный интерфейс (CLI).
2. Приглашение к вводу формируется из реальных данных ОС (пример: username@hostname:~$).
3. Простой парсер: разделяет ввод на команду и аргументы по пробелам.
4. Команды-заглушки ls, cd, которые выводят своё имя и аргументы.
5. Команда exit.
6. Обработка ошибок: неизвестная команда, пустой ввод, Ctrl+C, Ctrl+D.
7. Демонстрация работы (см. пример ниже).
### Структура проекта (на данном этапе)

```text
.
├── run.sh                        # скрипт запуска
├── requirements.txt              # зависимости (pytest)
├── pytest.ini                    # конфигурация pytest
├── README.md                     # описание проекта
├── .gitignore
├── src/
│   ├── main.py                   # класс Pandi: REPL, парсер, диспетчер команд
│   └── commands/
│       ├── __init__.py           # реестр команд REGISTRY
│       ├── cmd_ls.py             # заглушка ls
│       └── cmd_cd.py             # заглушка cd
└── tests/
    ├── test_commands.py          # тесты функций команд
    ├── test_parser.py            # тесты парсера
    └── test_manager.py           # тесты диспетчера команд
```
### Реализованные команды

| Команда | Поведение |
|---------|-----------|
| `ls [args...]` | Заглушка. Выводит своё имя и аргументы. |
| `cd [args...]` | Заглушка. Выводит своё имя и аргументы. |
| `exit` | Завершает работу эмулятора. |

### Обработка ошибок

| Ситуация | Реакция |
|----------|---------|            
| Пустой ввод (только Enter) | Новый промпт, ничего не происходит |
| Неизвестная команда | `<cmd>: command not found` |
| `Ctrl+C (SIGINT) ` | Печать ^C, новый промпт, приложение продолжает работу |
| `Ctrl+D (EOF)` |Завершение работы, печать прощального сообщения |
| ` exit ` | Завершение работы с кодом 0 |

### Пример работы

```bash
user@host:~$ ls
ls
user@host:~$ ls -la /home
ls -la /home
user@host:~$ cd
cd
user@host:~$ cd /tmp
cd /tmp
user@host:~$ lol
lol: command not found
user@host:~$ ^C
^C
user@host:~$ exit
Session terminated.
```

## Этап 2. Конфигурация

Что добавлено:
1. Параметры командной строки:
   - `--vfs PATH` — путь к физическому расположению VFS (на этапе 2 только
     отображается в отладочном выводе, фактически будет использован на этапе 3).
   - `--script PATH` — путь к стартовому скрипту эмулятора.
2. Отладочный вывод всех заданных параметров при запуске:

   ```text
   [pandi] --- startup configuration ---
   [pandi] vfs_path    = './vfs/example.zip'
   [pandi] script_path = 'scripts/01_ok.pandi'
   [pandi] username    = 'venturn'
   [pandi] hostname    = 'venturn-expub'
   [pandi] -------------------------------
   ```
3. Выполнение стартового скрипта:
   - Пустые строки и строки, начинающиеся с `#`, пропускаются.
   - На экран выводится и «ввод» (промпт + команда), и её вывод —
     имитируя диалог с пользователем.
   - При первой же ошибке выполнение скрипта прекращается, печатается
     сообщение вида `pandi: script '<path>' stopped at line N`,
     процесс завершается с кодом 1.
   - После успешного выполнения скрипта эмулятор завершает работу
     с кодом 0 (в интерактивный REPL не переходит).
4. Три стартовых скрипта (`scripts/`), покрывающих все режимы команд этапа 1,
   включая обработку ошибок.
5. Сценарии запуска (`scenarios/`) с различными комбинациями параметров.

### Структура проекта (на данном этапе)

```text
.
├── run.sh                        # скрипт запуска
├── requirements.txt              # зависимости (pytest)
├── pytest.ini                    # конфигурация pytest
├── README.md                     # описание проекта
├── .gitignore
├── src/
│   ├── main.py                   # точка входа, реэкспорт Pandi/build_arg_parser
│   ├── cli.py                    # build_arg_parser (argparse)
│   ├── shell.py                  # класс Pandi: REPL, парсер, диспетчер команд
│   ├── script.py                 # run_script (стартовый скрипт)
│   └── commands/
│       ├── __init__.py           # реестр команд REGISTRY
│       ├── errors.py             # CommandError
│       ├── cmd_ls.py             # заглушка ls
│       └── cmd_cd.py             # заглушка cd
├── scripts/                      # стартовые скрипты эмулятора
│   ├── 01_ok.pandi               # все команды успешно
│   ├── 02_error.pandi            # остановка на ошибке
│   └── 03_comments.pandi         # комментарии и пустые строки
├── scenarios/                    # сценарии запуска
│   ├── demo_no_args.sh           # без параметров — обычный REPL
│   ├── demo_vfs_only.sh          # только --vfs
│   ├── demo_script_only.sh       # только --script
│   ├── demo_both.sh              # --vfs и --script одновременно
│   └── demo_script_notfound.sh   # несуществующий скрипт
└── tests/
    ├── test_commands.py          # тесты функций команд
    ├── test_parser.py            # тесты парсера
    ├── test_manager.py           # тесты диспетчера команд
    ├── test_config.py            # тесты argparse и отладочного вывода
    └── test_script.py            # тесты выполнения скриптов
```

### Параметры командной строки

| Параметр          | Назначение                                                      |
|-------------------|-----------------------------------------------------------------|
| `--vfs PATH`      | Путь к физическому расположению VFS (используется на этапе 3). |
| `--script PATH`   | Путь к стартовому скрипту эмулятора.                            |

### Формат стартового скрипта

- Одна команда — одна строка.
- Пустые строки игнорируются.
- Строки, начинающиеся с `#` (после возможных пробелов), — комментарии.
- При первой же ошибочной команде выполнение прекращается.

Пример (`scripts/01_ok.pandi`):

```text
# Успешное выполнение всех команд
ls
ls -la /home
cd
cd /tmp
exit
```

### Примеры запуска

```bash
# Обычный REPL
./run.sh

# Только VFS (REPL + отладочный вывод конфигурации)
./run.sh --vfs ./vfs/example.zip

# Только скрипт
./run.sh --script scripts/01_ok.pandi

# Оба параметра
./run.sh --vfs ./vfs/example.zip --script scripts/03_comments.pandi

# Скрипт с ошибкой — остановка на первой ошибке, exit code 1
./run.sh --script scripts/02_error.pandi
```

Все перечисленные комбинации собраны как исполняемые сценарии в
каталоге `scenarios/`.

## Этап 3. VFS (виртуальная файловая система)

На этом этапе эмулятор научился работать с виртуальной файловой
системой, которая хранится в ZIP-архиве и загружается целиком в
память (без распаковки на диск).

### Что добавлено

- Модуль [src/vfs.py](src/vfs.py) — загрузка VFS из ZIP, представление
  дерева в памяти, получение `motd`.
- Поддержка приветствия `motd`: если в корне VFS есть файл с таким
  именем, его содержимое печатается при старте.
- Обработка ошибок загрузки VFS: сообщение `pandi: cannot load vfs ...`
  с кодом возврата 1, без traceback.
- Генератор ZIP-архивов [tools/make_vfs.py](tools/make_vfs.py) —
  воспроизводимо создаёт все архивы в `vfs/`.
- Четыре готовых VFS-архива в [vfs/](vfs/).
- Стартовые скрипты этапа 3 и сценарии реальной ОС, покрывающие
  минимальный, несколько файлов и глубокий (≥3 уровня) варианты.

### Представление VFS

Дерево из вложенных словарей:

```python
# директория: {"__dir": True, "children": {"name": node, ...}}
# файл:       {"__dir": False, "data": b"bytes"}
```

Корень — директория. Промежуточные директории создаются
автоматически для путей вида `a/b/c/file.txt`, даже если в ZIP нет
отдельных записей для `a/` и `a/b/`.

Все данные читаются через `zipfile.ZipFile.read(name)`; `extract`
и `extractall` не используются.

### VFS-архивы (`vfs/`)

| Архив              | Содержимое                                                                   |
|--------------------|------------------------------------------------------------------------------|
| `vfs/minimal.zip`  | `hello.txt` — минимальный VFS из одного файла.                               |
| `vfs/few.zip`      | `a.txt`, `b.txt`, `docs/readme.txt`, `docs/nested.txt`.                      |
| `vfs/deep.zip`     | `motd`, `a/top.txt`, `a/b/other.txt`, `a/b/c/file.txt`, `a/b/c/other.txt`.    |
| `vfs/motd.zip`     | `motd`, `readme.txt` — отдельный архив для проверки вывода приветствия.      |

Пересоздать архивы:

```bash
python3 tools/make_vfs.py
```

### Стартовые скрипты этапа 3

- [scripts/04_vfs_ok.pandi](scripts/04_vfs_ok.pandi) — все команды
  выполняются успешно (`ls`, `cd`, `exit`, перебор аргументов).
- [scripts/04_vfs_error.pandi](scripts/04_vfs_error.pandi) —
  неизвестная команда посередине, выполнение останавливается.

### Структура проекта (на данном этапе)

```text
.
├── run.sh                        # скрипт запуска
├── requirements.txt              # зависимости (pytest)
├── pytest.ini                    # конфигурация pytest
├── README.md                     # описание проекта
├── .gitignore
├── src/
│   ├── main.py                   # точка входа, реэкспорт Pandi/build_arg_parser
│   ├── cli.py                    # build_arg_parser (argparse)
│   ├── shell.py                  # класс Pandi: + загрузка VFS и motd
│   ├── script.py                 # run_script (стартовый скрипт)
│   ├── vfs.py                    # НОВЫЙ: VfsError, load_vfs, get_motd
│   └── commands/
│       ├── __init__.py           # реестр команд REGISTRY
│       ├── errors.py             # CommandError
│       ├── cmd_ls.py             # заглушка ls
│       └── cmd_cd.py             # заглушка cd
├── tools/
│   └── make_vfs.py               # НОВЫЙ: генератор ZIP-архивов
├── vfs/                          # НОВЫЙ: VFS-архивы
│   ├── minimal.zip               # минимальный VFS (1 файл)
│   ├── few.zip                   # несколько файлов + папка
│   ├── deep.zip                  # глубокий VFS (>=3 уровня) + motd
│   └── motd.zip                  # VFS с приветствием motd
├── scripts/                      # стартовые скрипты эмулятора
│   ├── 01_ok.pandi               # все команды успешно
│   ├── 02_error.pandi            # остановка на ошибке
│   ├── 03_comments.pandi         # комментарии и пустые строки
│   ├── 04_vfs_ok.pandi           # НОВЫЙ: все команды с VFS успешно
│   └── 04_vfs_error.pandi        # НОВЫЙ: ошибка с VFS
├── scenarios/                    # сценарии запуска
│   ├── demo_no_args.sh           # без параметров — обычный REPL
│   ├── demo_vfs_only.sh          # только --vfs
│   ├── demo_script_only.sh       # только --script
│   ├── demo_both.sh              # --vfs и --script одновременно
│   ├── demo_script_error.sh      # скрипт с ошибкой
│   ├── demo_script_notfound.sh   # несуществующий скрипт
│   ├── vfs_minimal.sh            # НОВЫЙ: минимальный VFS
│   ├── vfs_few.sh                # НОВЫЙ: несколько файлов
│   ├── vfs_deep.sh               # НОВЫЙ: глубокий VFS
│   ├── vfs_motd.sh               # НОВЫЙ: проверка motd
│   ├── vfs_notfound.sh           # НОВЫЙ: VFS не найден
│   └── vfs_bad.sh                # НОВЫЙ: битый ZIP-архив
└── tests/
    ├── test_commands.py          # тесты функций команд
    ├── test_parser.py            # тесты парсера
    ├── test_manager.py           # тесты диспетчера команд
    ├── test_config.py            # тесты argparse и отладочного вывода
    ├── test_script.py            # тесты выполнения скриптов
    └── test_vfs.py               # НОВЫЙ: тесты загрузки VFS и motd
```

### Примеры запуска с VFS

```bash
# Пересоздать VFS-архивы
python3 tools/make_vfs.py

# Минимальный VFS + стартовый скрипт
./run.sh --vfs vfs/minimal.zip --script scripts/04_vfs_ok.pandi

# Несколько файлов
./run.sh --vfs vfs/few.zip --script scripts/04_vfs_ok.pandi

# Глубокий VFS (>=3 уровня) с motd
./run.sh --vfs vfs/deep.zip --script scripts/04_vfs_ok.pandi

# Только motd (интерактив)
printf 'exit\n' | ./run.sh --vfs vfs/motd.zip

# Ошибка: файл не найден (rc=1)
./run.sh --vfs /no/such/file.zip; echo rc=$?

# Ошибка: неверный формат (rc=1)
echo "not a zip" > /tmp/bad.zip
./run.sh --vfs /tmp/bad.zip; echo rc=$?
```

Готовые сценарии: `scenarios/vfs_minimal.sh`, `scenarios/vfs_few.sh`,
`scenarios/vfs_deep.sh`, `scenarios/vfs_motd.sh`,
`scenarios/vfs_notfound.sh`, `scenarios/vfs_bad.sh`.

### О коммите ZIP-архивов

Задание варианта 12 требует использовать ZIP-архив как источник
VFS. Поэтому `vfs/*.zip` коммитятся в репозиторий как **данные
задания**, а не как случайные бинарные артефакты. Для
воспроизводимости рядом лежит генератор `tools/make_vfs.py`,
который пересоздаёт все архивы одной командой.

## Этап 4. Основные команды

На этом этапе эмулятор получил настоящие рабочие команды,
опирающиеся на VFS из этапа 3: навигацию по дереву (`ls`, `cd`)
и две вспомогательные (`date`, `history`).

### Что добавлено

- Текущий каталог сессии (`shell._cwd`), начальное значение `/`.
- История введённых команд (`shell._history`): пополняется и в
  интерактивном режиме, и при выполнении стартового скрипта.
- Утилиты пути в [src/vfs.py](src/vfs.py): `resolve(cwd, path)` —
  нормализация с учётом `.`, `..`, абсолютных и относительных
  путей; `get_node(vfs, abspath)` — поиск узла по абсолютному пути.
- Четыре команды поверх VFS:

| Команда | Поведение |
|---------|-----------|
| `ls [path]` | Вывод содержимого каталога (отсортировано). Без аргумента — текущий каталог. Для файла печатает его имя. Флаги вида `-la` игнорируются (как заглушка `ls`). Ошибки: `ls: cannot access '<path>': No such file or directory`. |
| `cd [path]` | Переход в каталог. Без аргумента — переход в `/`. Поддерживает `..`, `.`, абсолютные и относительные пути. Ошибки: `cd: <path>: No such file or directory`, `cd: <path>: Not a directory`. |
| `date` | Печать текущей даты в формате `Day Mon DD HH:MM:SS TZ YYYY`. |
| `history` | Печать истории команд пронумерованным списком (как в bash). |

- Обработчики команд теперь принимают `shell` вторым параметром
  (регистр `REGISTRY` вызывает их через диспетчер `_command_manager`).
  При запуске без `--vfs` команды `ls`/`cd` работают как прежние
  заглушки, чтобы не ломать поведение этапов 1–2.
- Стартовые скрипты этапа 4 и сценарий демонстрации.

### Стартовые скрипты этапа 4

- [scripts/05_main_ok.pandi](scripts/05_main_ok.pandi) — полный
  обход `deep.zip`: `ls`, `cd`, `..`, `date`, `history`.
- [scripts/05_main_err_nopath.pandi](scripts/05_main_err_nopath.pandi) —
  `cd` в несуществующий каталог, остановка скрипта.
- [scripts/05_main_err_notdir.pandi](scripts/05_main_err_notdir.pandi) —
  `cd` в файл, ошибка `Not a directory`.

Готовый сценарий демонстрации: [scenarios/demo_stage4.sh](scenarios/demo_stage4.sh).

### Примеры запуска

```bash
# Успешный проход по глубокому VFS
./run.sh --vfs vfs/deep.zip --script scripts/05_main_ok.pandi

# Ошибка: нет такого пути (rc=1)
./run.sh --vfs vfs/deep.zip --script scripts/05_main_err_nopath.pandi

# Ошибка: не каталог (rc=1)
./run.sh --vfs vfs/deep.zip --script scripts/05_main_err_notdir.pandi

# Полная демонстрация этапа 4 на нескольких VFS
bash scenarios/demo_stage4.sh
```

### Структура проекта (на данном этапе)

```text
.
├── run.sh                        # скрипт запуска
├── requirements.txt              # зависимости (pytest)
├── pytest.ini                    # конфигурация pytest
├── README.md                     # описание проекта
├── .gitignore
├── src/
│   ├── main.py                   # точка входа, реэкспорт Pandi/build_arg_parser
│   ├── cli.py                    # build_arg_parser (argparse)
│   ├── shell.py                  # класс Pandi: + _cwd, _history
│   ├── script.py                 # run_script (стартовый скрипт) + _history
│   ├── vfs.py                    # VfsError, load_vfs, get_motd + resolve, get_node
│   └── commands/
│       ├── __init__.py           # реестр команд REGISTRY
│       ├── errors.py             # CommandError
│       ├── cmd_ls.py             # ls по VFS
│       ├── cmd_cd.py             # cd по VFS
│       ├── cmd_date.py           # НОВЫЙ: date
│       └── cmd_history.py        # НОВЫЙ: history
├── tools/
│   └── make_vfs.py               # генератор ZIP-архивов
├── vfs/                          # VFS-архивы
│   ├── minimal.zip               # минимальный VFS (1 файл)
│   ├── few.zip                   # несколько файлов + папка
│   ├── deep.zip                  # глубокий VFS (>=3 уровня) + motd
│   └── motd.zip                  # VFS с приветствием motd
├── scripts/                      # стартовые скрипты эмулятора
│   ├── 01_ok.pandi               # все команды успешно
│   ├── 02_error.pandi            # остановка на ошибке
│   ├── 03_comments.pandi         # комментарии и пустые строки
│   ├── 04_vfs_ok.pandi           # все команды с VFS успешно
│   ├── 04_vfs_error.pandi        # ошибка с VFS
│   ├── 05_main_ok.pandi          # НОВЫЙ: все команды этапа 4 с VFS успешно
│   ├── 05_main_err_nopath.pandi  # НОВЫЙ: cd в несуществующий путь
│   └── 05_main_err_notdir.pandi  # НОВЫЙ: cd в файл (Not a directory)
├── scenarios/                    # сценарии запуска
│   ├── demo_no_args.sh           # без параметров — обычный REPL
│   ├── demo_vfs_only.sh          # только --vfs
│   ├── demo_script_only.sh       # только --script
│   ├── demo_both.sh              # --vfs и --script одновременно
│   ├── demo_script_error.sh      # скрипт с ошибкой
│   ├── demo_script_notfound.sh   # несуществующий скрипт
│   ├── vfs_minimal.sh            # минимальный VFS
│   ├── vfs_few.sh                # несколько файлов
│   ├── vfs_deep.sh               # глубокий VFS
│   ├── vfs_motd.sh               # проверка motd
│   ├── vfs_notfound.sh           # VFS не найден
│   ├── vfs_bad.sh                # битый ZIP-архив
│   └── demo_stage4.sh            # НОВЫЙ: демонстрация ls/cd/date/history
└── tests/
    ├── test_commands.py          # тесты функций команд
    ├── test_parser.py            # тесты парсера
    ├── test_manager.py           # тесты диспетчера команд
    ├── test_config.py            # тесты argparse и отладочного вывода
    ├── test_script.py            # тесты выполнения скриптов
    ├── test_vfs.py               # тесты VFS (этап 3)
    └── test_stage4.py            # НОВЫЙ: тесты ls/cd/date/history, resolve/get_node
```

## Тесты

### Запуск тестов
```bash
pytest -v
```

Ожидается 63 пройденных теста (этапы 1, 2, 3 и 4 вместе).