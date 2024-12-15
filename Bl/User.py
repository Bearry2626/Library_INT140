from typing import List, Dict

class User:
    def __init__(self, name: str, password: str, role: str = "user"):
        self.name = name
        self.password = password
        self.role = role
        self.borrowed_books: List[Dict[str, str]] = []
