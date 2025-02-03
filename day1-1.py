from dataclasses import dataclass
from enum import Enum
from typing import Optional

db = ['Linux', 'Windows', 'MacOS', 'ubuntu', 'redhat', 'test']

@dataclass
class User:
    loginId: str
    name: str
    age: int
    emai: str

# ProductCategory.ELECTRONICS
class ProductCategory(Enum):
    ELECTRONICS = 'electronics'
    CLOTHING = 'clothing'
    HOME = 'home'

# Optianl: None이나 list를 반환할 수 있음
def get_product(page: int=1, per_page: int=2) -> Optional(list): # type: ignore
    if type(page) != int:
        return None
    startIdx = (page - 1) * per_page
    endIdx = startIdx + per_page
    return db[startIdx:endIdx]

