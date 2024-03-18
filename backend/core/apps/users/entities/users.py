from dataclasses import dataclass


@dataclass
class User:
    id: str # noqa
    email: str
    password: str

    first_name: str
    last_name: str
