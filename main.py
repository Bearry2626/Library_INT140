from Ui.LibraryUI import LibraryUI

def main():
    ui = LibraryUI()
    
    # Initial Admin
    ui.library_bl.register_user("admin", "admin", "admin")

    # Initial Categories
    ui.library_bl.add_category("Programming")
    ui.library_bl.add_category("Science Fiction")
    ui.library_bl.add_category("Fantasy")
    
    # Initial books
    ui.library_bl.add_book("Python 101", "Michael Driscoll", "Programming")
    ui.library_bl.add_book("The Martian", "Andy Weir", "Science Fiction")
    ui.library_bl.add_book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy")
    ui.library_bl.add_book("Supakorn", "github.com/supakornn", "Programming")
    ui.run()

if __name__ == "__main__":
    main()
