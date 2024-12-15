import unittest
from Bl.LibraryBl import LibraryBl
from Bl.User import User
from Bl.Book import Book

class TestLibraryBl(unittest.TestCase):
    def setUp(self):
        self.library_bl = LibraryBl()
        self.library_bl.register_user("admin", "admin", "admin")

    def test_register_user(self):
        self.library_bl.register_user("user1", "password1")
        self.assertEqual(len(self.library_bl.users), 2)
        with self.assertRaises(ValueError):
            self.library_bl.register_user("", "password")
        with self.assertRaises(ValueError):
            self.library_bl.register_user("user1", "password1")

    def test_login_user(self):
        self.assertTrue(self.library_bl.login_user("admin", "admin"))
        self.assertFalse(self.library_bl.login_user("admin", "wrongpassword"))
        with self.assertRaises(ValueError):
            self.library_bl.login_user("", "password")

    def test_add_book(self):
        self.library_bl.add_book("Book1", "Author1", "Category1")
        self.assertEqual(len(self.library_bl.books), 1)
        with self.assertRaises(ValueError):
            self.library_bl.add_book("", "Author1", "Category1")
        with self.assertRaises(ValueError):
            self.library_bl.add_book("Book1", "", "Category1")
        with self.assertRaises(ValueError):
            self.library_bl.add_book("Book1", "Author1", "")

    def test_add_category(self):
        self.library_bl.add_category("Category1")
        self.assertEqual(len(self.library_bl.categories), 1)
        with self.assertRaises(ValueError):
            self.library_bl.add_category("")

    def test_borrow_book(self):
        self.library_bl.add_book("Book1", "Author1", "Category1")
        self.library_bl.login_user("admin", "admin")
        self.library_bl.logged_in_user.borrowed_books = []
        borrow_date_str = "2023-10-01"
        message = self.library_bl.borrow_book("Book1", borrow_date_str)
        self.assertIn("has been borrowed", message)
        with self.assertRaises(ValueError):
            self.library_bl.borrow_book("", borrow_date_str)
        with self.assertRaises(ValueError):
            self.library_bl.borrow_book("Book1", "")
        with self.assertRaises(ValueError):
            self.library_bl.borrow_book("Book1", "invalid-date")
        with self.assertRaises(PermissionError):
            self.library_bl.logged_in_user = None
            self.library_bl.borrow_book("Book1", borrow_date_str)

    def test_return_book(self):
        self.library_bl.add_book("Book1", "Author1", "Category1")
        self.library_bl.login_user("admin", "admin")
        borrow_date_str = "2023-10-01"
        self.library_bl.borrow_book("Book1", borrow_date_str)
        return_date_str = "2023-10-20"
        message = self.library_bl.return_book("Book1", return_date_str)
        self.assertIn("has been returned", message)
        self.assertIn("fine", message)
        with self.assertRaises(ValueError):
            self.library_bl.return_book("", return_date_str)
        with self.assertRaises(ValueError):
            self.library_bl.return_book("Book1", "")
        with self.assertRaises(ValueError):
            self.library_bl.return_book("Book1", "invalid-date")
        with self.assertRaises(PermissionError):
            self.library_bl.logged_in_user = None
            self.library_bl.return_book("Book1", return_date_str)

    def test_calculate_fine(self):
        self.library_bl.add_book("Book1", "Author1", "Category1")
        self.library_bl.login_user("admin", "admin")
        borrow_date_str = "2023-10-01"
        self.library_bl.borrow_book("Book1", borrow_date_str)
        current_date_str = "2023-10-20"
        fine = self.library_bl.calculate_fine(self.library_bl.logged_in_user, "Book1", current_date_str)
        self.assertEqual(fine, 5.0)
        with self.assertRaises(ValueError):
            self.library_bl.calculate_fine(self.library_bl.logged_in_user, "", current_date_str)
        with self.assertRaises(ValueError):
            self.library_bl.calculate_fine(self.library_bl.logged_in_user, "Book1", "invalid-date")

    def test_check_available_books(self):
        self.library_bl.add_book("Book1", "Author1", "Category1")
        available_books = self.library_bl.check_available_books()
        self.assertEqual(len(available_books), 1)
        self.assertEqual(available_books[0]["title"], "Book1")

    def test_search_books(self):
        self.library_bl.add_book("Book1", "Author1", "Category1")
        search_results = self.library_bl.search_books("Book1")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]["title"], "Book1")
        search_results = self.library_bl.search_books("Author1")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]["author"], "Author1")
        search_results = self.library_bl.search_books("Category1")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]["category"], "Category1")

    def test_generate_report(self):
        self.library_bl.add_book("Book1", "Author1", "Category1")
        report = self.library_bl.generate_report()
        self.assertEqual(report["total_books"], 1)
        self.assertEqual(report["borrowed_books"], 0)
        self.assertEqual(report["available_books"], 1)
        self.assertEqual(report["categories"], 0)

if __name__ == "__main__":
    unittest.main()
