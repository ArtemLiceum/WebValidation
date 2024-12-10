from pydantic import BaseModel
from typing import Dict

class Template(BaseModel):
    name: str
    fields: Dict[str, str]

    def __str__(self):
        return f"Template(name={self.name}, fields={self.fields})"
