import unittest
from unittest.mock import patch
from pathlib import Path
from library import Library, Status, SearchCriteria


class TestLibrary(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый экземпляр библиотеки с тестовым файлом данных
        self.test_data_file = Path("test_books.json")
        self.library = Library(data_file=self.test_data_file)

    def tearDown(self):
        # Удаляем тестовый файл данных после выполнения тестов
        if self.test_data_file.exists():
            self.test_data_file.unlink()

    def test_load_from_file(self):
        self.library.books = []
        self.library.save_to_file()  # Сохраняем текущие данные
        book = self.library.add_book("Тестовая книга", "Автор", 2023)
        self.library.load_from_file()  # Загружаем их обратно
        self.assertEqual(len(self.library.books), 1)  # Ожидаем одну книгу
        self.assertEqual(self.library.books[0].title, "Тестовая книга")

    def test_add_book(self):
        book = self.library.add_book("Тестовая книга", "Автор", 2023)
        self.assertEqual(book.title, "Тестовая книга")
        self.assertEqual(book.author, "Автор")
        self.assertEqual(book.year, 2023)
        self.assertEqual(book.status, Status.AVAILABLE)
        self.assertEqual(book.id, 1)

    def test_delete_book(self):
        book = self.library.add_book("Удаляемая книга", "Автор", 2022)
        self.library.delete_book(book.id)
        self.assertIsNone(self.library.get_book_by_id(book.id))

    def test_search_books(self):
        book1 = self.library.add_book("Python 101", "Автор 1", 2020)
        book2 = self.library.add_book("Python 102", "Автор 2", 2021)

        # Поиск по названию
        found_books = self.library.search_books(SearchCriteria.TITLE, "Python 101")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "Python 101")

        # Поиск по автору
        found_books = self.library.search_books(SearchCriteria.AUTHOR, "Автор 2")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].author, "Автор 2")

        # Поиск по году
        found_books = self.library.search_books(SearchCriteria.YEAR, "2020")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].year, 2020)

    def test_change_status(self):
        book = self.library.add_book("Книга для теста", "Автор", 2021)
        updated_book = self.library.change_status(book.id, Status.ISSUED)
        self.assertEqual(updated_book.status, Status.ISSUED)

    def test_add_book_validation(self):
        with self.assertRaises(ValueError):
            self.library.add_book("", "Автор", 2021)  # Пустое название
        with self.assertRaises(ValueError):
            self.library.add_book("Книга", "", 2021)  # Пустой автор
        with self.assertRaises(ValueError):
            self.library.add_book("Книга", "Автор", -1)  # Неверный год

    def test_save_to_file_error(self):
        def mock_open(*args, **kwargs):
            raise IOError("Ошибка при сохранении файла")

        with unittest.mock.patch("pathlib.Path.open", mock_open):
            with self.assertRaises(ValueError):
                self.library.save_to_file()

    def test_change_status_invalid(self):
        # Попытка изменить статус книги с несуществующим ID
        with self.assertRaises(ValueError):
            self.library.change_status(999, Status.AVAILABLE)

        # Передача некорректного статуса (не экземпляр Status)
        book = self.library.add_book("Книга", "Автор", 2022)
        with self.assertRaises(TypeError):
            self.library.change_status(book.id, "Некорректный статус")


if __name__ == "__main__":
    unittest.main()
