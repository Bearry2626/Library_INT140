from Bl.LibraryBl import LibraryBl
from Bl.User import User

class LibraryUI:
    def __init__(self):
        self.library_bl = LibraryBl()

    def run(self):
        while True:
            print("\nWelcome to the Library")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.register()
            elif choice == '2':
                if self.login():
                    self.show_menu()
            elif choice == '3':
                break
            else:
                print("Invalid choice, please try again.")

    def show_menu(self):
        while True:
            print("\nLibrary Menu")
            if self.library_bl.logged_in_user.name == "admin":
                print("1. Add a book")
                print("2. Add a category")
                print("3. List all books")
                print("4. Borrow a book")
                print("5. Return a book")
                print("6. Calculate fine")
                print("7. Check available books")
                print("8. Search books")
                print("9. Generate report")
                print("10. Logout")
            else:
                print("1. List all books")
                print("2. Borrow a book")
                print("3. Return a book")
                print("4. Check available books")
                print("5. Search books")
                print("6. Logout")
            choice = input("Enter your choice: ")
            if self.library_bl.logged_in_user.name == "admin":
                if choice == '1':
                    self.add_book()
                elif choice == '2':
                    self.add_category()
                elif choice == '3':
                    self.list_books()
                elif choice == '4':
                    self.borrow_book()
                elif choice == '5':
                    self.return_book()
                elif choice == '6':
                    self.calculate_fine()
                elif choice == '7':
                    self.check_available_books()
                elif choice == '8':
                    self.search_books()
                elif choice == '9':
                    self.generate_report()
                elif choice == '10':
                    break
                else:
                    print("Invalid choice, please try again.")
            else:
                if choice == '1':
                    self.list_books()
                elif choice == '2':
                    self.borrow_book()
                elif choice == '3':
                    self.return_book()
                elif choice == '4':
                    self.check_available_books()
                elif choice == '5':
                    self.search_books()
                elif choice == '6':
                    break
                else:
                    print("Invalid choice, please try again.")

    def register(self):
        print("\nRegister a new user")
        name = input("Enter user name: ")
        password = input("Enter password: ")
        if not name or not password:
            print("Error: Name and password cannot be empty.")
            return
        self.library_bl.register_user(name, password)
        print("User registered successfully.")

    def login(self):
        print("\nLogin")
        name = input("Enter user name: ")
        password = input("Enter password: ")
        if not name or not password:
            print("Error: Name and password cannot be empty.")
            return False
        if self.library_bl.login_user(name, password):
            print("Login successfully.")
            return True
        else:
            print("Invalid user name or password.")
            return False

    def add_book(self):
        print("\nAdd a new book")
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        category = input("Enter book category: ")
        if not title or not author or not category:
            print("Error: Title, author, and category cannot be empty.")
            return
        self.library_bl.add_book(title, author, category)
        print("Book added successfully.")

    def add_category(self):
        print("\nAdd a new category")
        category = input("Enter category name: ")
        if not category:
            print("Error: Category cannot be empty.")
            return
        self.library_bl.add_category(category)
        print("Category added successfully.")

    def list_books(self):
        print("\nList of all books")
        books = self.library_bl.list_books()
        for book in books:
            print(f"Title: {book['title']}, Author: {book['author']}, Category: {book['category']}, Status: {book['status']}")

    def borrow_book(self):
        print("\nBorrow a book")
        title = input("Enter book title to borrow: ")
        borrow_date_str = input("Enter borrow date (YYYY-MM-DD): ")
        if not title or not borrow_date_str:
            print("Error: Title and borrow date cannot be empty.")
            return
        try:
            message = self.library_bl.borrow_book(title, borrow_date_str)
            print(message)
        except ValueError as e:
            print(f"Error: {e}")
        except PermissionError as e:
            print(f"Error: {e}")

    def return_book(self):
        print("\nReturn a book")
        if not self.library_bl.logged_in_user.borrowed_books:
            print("You have no borrowed books.")
            return
        print("Books you have borrowed:")
        for book in self.library_bl.logged_in_user.borrowed_books:
            print(f"Title: {book['title']}, Author: {book['author']}")
        title = input("Enter book title to return: ")
        return_date_str = input("Enter return date (YYYY-MM-DD): ")
        if not title or not return_date_str:
            print("Error: Title and return date cannot be empty.")
            return
        try:
            message = self.library_bl.return_book(title, return_date_str)
            print(message)
        except ValueError as e:
            print(f"Error: {e}")
        except PermissionError as e:
            print(f"Error: {e}")

    def calculate_fine(self):
        print("\nCalculate fine")
        title = input("Enter book title to calculate fine: ")
        current_date_str = input("Enter current date (YYYY-MM-DD): ")
        if not title or not current_date_str:
            print("Error: Title and current date cannot be empty.")
            return
        try:
            fine = self.library_bl.calculate_fine(self.library_bl.logged_in_user, title, current_date_str)
            print(f"The fine for {title} is ${fine:.2f}")
        except ValueError as e:
            print(f"Error: {e}")

    def check_available_books(self):
        print("\nCheck available books")
        books = self.library_bl.check_available_books()
        for book in books:
            print(f"Title: {book['title']}, Author: {book['author']}, Category: {book['category']}")

    def search_books(self):
        print("\nSearch books")
        query = input("Enter search query (title, author, or category): ")
        books = self.library_bl.search_books(query)
        for book in books:
            print(f"Title: {book['title']}, Author: {book['author']}, Category: {book['category']}, Status: {book['status']}")

    def generate_report(self):
        print("\nGenerate report")
        report = self.library_bl.generate_report()
        print(f"Total books: {report['total_books']}")
        print(f"Borrowed books: {report['borrowed_books']}")
        print(f"Available books: {report['available_books']}")
        print(f"Categories: {report['categories']}")
