from dataclasses import dataclass

@dataclass
class Domain:
    name: str
    key: str
    secret: str
    partner: str
    is_disabled: bool
