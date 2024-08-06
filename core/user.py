from dataclasses import dataclass

@dataclass
class User:
    username: str
    is_admin: bool