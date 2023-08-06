from dataclasses import dataclass

@dataclass
class Lti:
    title: str
    identifier: str
    is_disabled: bool
