from typing import List, Dict, Optional
from datetime import datetime, timedelta

class Book:
    def __init__(self, title: str, author: str, category: str):
        self.title = title
        self.author = author
        self.category = category
        self.status = "available"
        self.borrowed_date: Optional[datetime] = None
