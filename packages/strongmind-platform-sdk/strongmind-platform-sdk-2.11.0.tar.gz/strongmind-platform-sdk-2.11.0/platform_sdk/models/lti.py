from dataclasses import dataclass

@dataclass
class Lti:
    id: int
    title: str
    identifier: str
    is_disabled: bool
