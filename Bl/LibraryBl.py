from typing import List, Dict, Optional
from Bl.User import User
from Bl.Book import Book

class LibraryBl:
    def __init__(self):
        self.books: List[Book] = []
        self.users: List[User] = []
        self.categories: List[str] = []
        self.logged_in_user: Optional[User] = None

    def register_user(self, name: str, password: str, role: str = "user") -> None:
        if not name or not password:
            raise ValueError("Name and password cannot be empty.")
        if any(user.name == name for user in self.users):
            raise ValueError("User already exists.")
        self.users.append(User(name, password, role))

    def login_user(self, name: str, password: str) -> bool:
        if not name or not password:
            raise ValueError("Name and password cannot be empty.")
        for user in self.users:
            if user.name == name and user.password == password:
                self.logged_in_user = user
                return True
        return False

    def add_book(self, title: str, author: str, category: str) -> None:
        if not title or not author or not category:
            raise ValueError("Title, author, and category cannot be empty.")
        self.books.append(Book(title, author, category))

    def add_category(self, category: str) -> None:
        if not category:
            raise ValueError("Category cannot be empty.")
        if category not in self.categories:
            self.categories.append(category)

    def list_books(self) -> List[Dict[str, str]]:
        return [{"title": book.title, "author": book.author, "category": book.category, "status": book.status} for book in self.books]

    def borrow_book(self, title: str, borrow_date_str: str) -> Optional[str]:
        if not self.logged_in_user:
            raise PermissionError("Please log in first.")
        if not title:
            raise ValueError("Title cannot be empty.")
        if not self._validate_date_format(borrow_date_str):
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        for book in self.books:
            if book.title == title and book.status == "available":
                book.status = "borrowed"
                book.borrowed_date = borrow_date_str
                self.logged_in_user.borrowed_books.append({"title": book.title, "author": book.author, "borrowed_date": borrow_date_str})
                return f"{title} has been borrowed by {self.logged_in_user.name}."
        return f"{title} is not available."

    def return_book(self, title: str, return_date_str: str) -> Optional[str]:
        if not self.logged_in_user:
            raise PermissionError("Please log in first.")
        if not title:
            raise ValueError("Title cannot be empty.")
        if not self._validate_date_format(return_date_str):
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        for book in self.books:
            if book.title == title and book.status == "borrowed":
                book.status = "available"
                borrowed_date_str = next(b["borrowed_date"] for b in self.logged_in_user.borrowed_books if b["title"] == title)
                days_borrowed = self._calculate_days_between(borrowed_date_str, return_date_str)
                book.borrowed_date = None
                self.logged_in_user.borrowed_books = [b for b in self.logged_in_user.borrowed_books if b["title"] != title]
                if days_borrowed > 14:
                    fine = (days_borrowed - 14) * 1.0
                    return f"{title} has been returned by {self.logged_in_user.name}. You have a fine of ${fine:.2f}."
                return f"{title} has been returned by {self.logged_in_user.name}."
        return f"{title} was not borrowed by {self.logged_in_user.name}."

    def _validate_date_format(self, date_str: str) -> bool:
        parts = date_str.split("-")
        if len(parts) != 3:
            return False
        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return False
        if not (1 <= int(month) <= 12):
            return False
        if not (1 <= int(day) <= 31):
            return False
        return True

    def _calculate_days_between(self, start_date_str: str, end_date_str: str) -> int:
        start_year, start_month, start_day = map(int, start_date_str.split("-"))
        end_year, end_month, end_day = map(int, end_date_str.split("-"))
        start_date = (start_year * 365) + (start_month * 30) + start_day
        end_date = (end_year * 365) + (end_month * 30) + end_day
        return end_date - start_date

    def calculate_fine(self, user: User, title: str, current_date_str: str) -> float:
        if not title:
            raise ValueError("Title cannot be empty.")
        if not self._validate_date_format(current_date_str):
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        for book in self.books:
            if book.title == title and book.status == "borrowed":
                borrowed_date_str = next(b["borrowed_date"] for b in user.borrowed_books if b["title"] == title)
                days_borrowed = self._calculate_days_between(borrowed_date_str, current_date_str)
                if days_borrowed > 14:
                    return (days_borrowed - 14) * 1.0
        return 0.0

    def check_available_books(self) -> List[Dict[str, str]]:
        return [{"title": book.title, "author": book.author, "category": book.category} for book in self.books if book.status == "available"]

    def search_books(self, query: str) -> List[Dict[str, str]]:
        return [{"title": book.title, "author": book.author, "category": book.category, "status": book.status} for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in book.category.lower()]

    def generate_report(self) -> Dict[str, int]:
        report = {
            "total_books": len(self.books),
            "borrowed_books": len([book for book in self.books if book.status == "borrowed"]),
            "available_books": len([book for book in self.books if book.status == "available"]),
            "categories": len(self.categories)
        }
        return report
