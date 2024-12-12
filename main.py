from library import Library, Status, SearchCriteria,Book
from typing import List


def display_books(books: List[Book], not_found_message: str = "Книги не найдены.")-> None:
    """Отображение списка книг."""
    if not books:
        print(not_found_message)
    else:
        for book in books:
            print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status.value}")

def main() -> None:
    """Основная функция для взаимодействия с пользователем."""
    library = Library()
    library.load_from_file()

    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход\n")

        choice = input("Выберите команду (1-6): \n")

        if choice == '1':
            try:
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                year = input("Введите год издания: ").strip()

                if not year.isdigit():
                    raise ValueError("Год должен быть числом.")

                year = int(year)
                added_book = library.add_book(title, author, year)
                print(f"Книга '{added_book.title}' успешно добавлена с ID {added_book.id}.")
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Произошла ошибка при добавлении книги: {e}")

        elif choice == '2':
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
                print(f"Книга с ID {book_id} успешно удалена.")
            except ValueError:
                print("Ошибка: ID книги должен быть числом. Попробуйте снова.")
            except Exception as e:
                print(f"Произошла ошибка при удалении книги: {e}")

        elif choice == '3':
            print(
                "Выберите критерий поиска:\n"
                    "\t1 - Название\n"
                    "\t2 - Автор\n"
                    "\t3 - Год")
            try:
                criteria_int = int(input("Введите номер критерия поиска: "))
                if criteria_int not in [1, 2, 3]:
                    print("Ошибка: Введите 1, 2 или 3 для выбора критерия.")
                    continue

                criteria = SearchCriteria(criteria_int)

                value = input("Введите значение для поиска: ").strip()
                if not value:
                    print("Ошибка: Значение для поиска не может быть пустым.")
                    continue
                found_books = library.search_books(criteria, value)
                display_books(found_books, not_found_message="По вашему запросу книги не найдены.")

            except ValueError:
                print("Ошибка: Неверный ввод.")

        elif choice == '4':
            display_books(library.books, not_found_message="В библиотеке пока нет книг.")

        elif choice == '5':
            try:
                book_id = int(input("Введите ID книги для изменения статуса: "))
                status_int = int(input("Введите новый статус ('0' - выдана, '1' - в наличии): "))

                if status_int in [0, 1]:
                    status = Status.ISSUED if status_int == 0 else Status.AVAILABLE
                else:
                    print("Ошибка: Некорректное значение статуса. Введите '1' для 'в наличии' или '0' для 'выдана'.")
                    continue

                updated_book = library.change_status(book_id, status)
                if updated_book:
                    print(f'Статус книги "{updated_book.title}" "{updated_book.status}".')
                else:
                    print(f'Книга с ID {book_id} не найдена.')
            except ValueError:
                print("Ошибка: Нужно ввести число.")
            except Exception as e:
                print(f"Произошла ошибка при изменении статуса книги: {e}")

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Ошибка: Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
