import json
from pathlib import Path
from typing import List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

DATA_FILE = 'books.json'


class SearchCriteria(Enum):
    TITLE = 1
    AUTHOR = 2
    YEAR = 3


class Status(Enum):
    AVAILABLE = "в наличии"
    ISSUED = "выдано"


@dataclass
class Book:
    title: str
    author: str
    year: int
    status: Status
    id: int | None = None


class Library:
    def __init__(self, data_file: str = DATA_FILE) -> None:
        self.data_file = data_file
        self.books: List[Book] = []

    def load_from_file(self) -> None:
        """Загрузка данных из файла в список книг."""
        try:
            file_path = Path(self.data_file)
            if file_path.exists():
                with file_path.open('r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.books = [
                        Book(
                            id=book["id"],
                            title=book["title"],
                            author=book["author"],
                            year=book["year"],
                            status=Status(book["status"])
                        )
                        for book in data
                    ]
            else:
                self.books = []  # Если файл не существует, создаем пустой список
        except json.JSONDecodeError:
            self.books = []  # Если данные повреждены, создаем пустой список

    def save_to_file(self) -> None:
        """Сохранение списка книг в файл."""
        try:
            file_path = Path(self.data_file)
            with file_path.open('w', encoding='utf-8') as file:
                json.dump(
                    [
                        {**book.__dict__, "status": book.status.value}
                        for book in self.books
                    ],
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
        except (IOError, OSError) as e:
            raise ValueError(f"Ошибка при сохранении данных в файл: {e}")

    def get_book_by_id(self, book_id: int) -> Book | None:
        """ Возвращает книгу по её ID. """
        return next((book for book in self.books if book.id == book_id), None)

    def generate_id(self) -> int:
        """Генерирует уникальный ID для новой книги."""
        return len(self.books) + 1 if not self.books else max(book.id for book in self.books) + 1

    def validate_book_input(self, title: str, author: str, year: int) -> None:
        """Проверка корректности введенных данных."""
        current_year = datetime.now().year
        if not title.strip():
            raise ValueError("Название книги не может быть пустым.")
        if not author.strip():
            raise ValueError("Автор книги не может быть пустым.")
        if year <= 0 or year > current_year + 1:
            raise ValueError(f"Год должен быть положительным числом, не превышающим {current_year + 1}.")

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавление книги в библиотеку."""
        self.validate_book_input(title, author, year)
        book_id = self.generate_id()
        new_book = Book(title=title, author=author, year=year, status=Status.AVAILABLE, id=book_id)
        self.books.append(new_book)
        self.save_to_file()
        return new_book

    def delete_book(self, book_id: int) -> None:
        """Удаление книги по ID."""
        book_to_delete = self.get_book_by_id(book_id)
        if not book_to_delete:
            raise ValueError(f"Книга с ID {book_id} не найдена.")
        self.books.remove(book_to_delete)
        self.save_to_file()

    def search_books(self, criteria: SearchCriteria, value: str) -> List[Book]:
        """ Ищет книги по заданному числовому критерию и значению."""
        if criteria == SearchCriteria.TITLE:
            found_books = [book for book in self.books if value.lower() in book.title.lower()]
        elif criteria == SearchCriteria.AUTHOR:
            found_books = [book for book in self.books if value.lower() in book.author.lower()]
        elif criteria == SearchCriteria.YEAR:
            found_books = [book for book in self.books if str(book.year) == value]
        return found_books

    def change_status(self, book_id: int, status: Status) -> Book | None:
        """Изменяет статус книги по её ID."""
        book_to_change = self.get_book_by_id(book_id)
        if not book_to_change:
            raise ValueError(f"Книга с ID {book_id} не найдена")

            # Проверка типа статуса
        if not isinstance(status, Status):
            raise TypeError("Неверный тип статуса")

        book_to_change.status = status
        self.save_to_file()

        return book_to_change


