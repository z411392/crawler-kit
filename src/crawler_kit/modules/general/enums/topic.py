from enum import Enum
from os import getenv


class Topic(str, Enum):
    Test = "Test"
    Pchome = "Pchome"
    Ebay = "Ebay"
    Amazon = "Amazon"
    Lazada = "Lazada"

    def __str__(self):
        return f"projects/{getenv('PROJECT_ID')}/topics/{self.value}"
