from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str
    id_admin: bool