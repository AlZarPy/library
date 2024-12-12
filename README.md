
# Library Management System

## Описание

Данное тестовое задание - консольное приложение для управления библиотекой книг. Оно позволяет добавлять, удалять, искать, отображать книги, а также изменять их статус. Каждая книга в системе имеет уникальный идентификатор, название, автора, год издания и статус (в наличии/выдана).

Подробное описание задания по [ссылке](https://pastebin.com/raw/katdfmXM)

## Основные возможности

- **Добавление книги**: Пользователь может добавить книгу в библиотеку, указав её название, автора и год издания.
- **Удаление книги**: Возможность удалить книгу по её уникальному ID.
- **Поиск книги**: Поиск книги по критериям: название, автор или год издания.
- **Отображение всех книг**: Отображение списка всех книг с их подробными данными.
- **Изменение статуса книги**: Изменение статуса книги на "в наличии" или "выдана".

## Структура проекта

Проект состоит из нескольких файлов:

1. **`library.py`**: основной файл, содержащий логику работы с библиотекой (добавление, удаление, поиск, изменение статуса и сохранение данных в файл).
2. **`main.py`**: файл, который предоставляет интерфейс для взаимодействия с пользователем, используя консоль.
3. **`test_library.py`**: набор тестов для проверки функциональности библиотеки.
4. **`books.json`**: базовая библиотека для тестирования и ознакомления с функционалом


## Описание функционала:

- **Добавление книги**: При добавлении новой книги программа запрашивает название, автора и год издания, проверяет их на корректность и сохраняет в файл с уникальным ID.
- **Удаление книги**: Для удаления книги необходимо указать её уникальный ID. Если книга с таким ID не найдена, будет выведено сообщение об ошибке.
- **Поиск книги**: Книгу можно найти по названию, автору или году издания. Результаты поиска выводятся в консоль.
- **Отображение всех книг**: Печатает список всех книг в библиотеке с их данными.
- **Изменение статуса**: Для изменения статуса книги на "в наличии" или "выдана" необходимо указать её ID и новый статус.

## Тестирование

Для тестирования функциональности библиотеки используйте файл `test_library.py`. Он содержит тесты для проверки основных операций, таких как добавление книги, удаление, поиск, изменение статуса и сохранение в файл.


