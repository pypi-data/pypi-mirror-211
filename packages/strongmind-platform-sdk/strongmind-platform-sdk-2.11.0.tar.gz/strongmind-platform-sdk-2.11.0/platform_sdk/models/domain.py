from dataclasses import dataclass

@dataclass
class Domain:
    id: int
    name: str
    key: str
    secret: str
    partner: str
    is_disabled: bool
