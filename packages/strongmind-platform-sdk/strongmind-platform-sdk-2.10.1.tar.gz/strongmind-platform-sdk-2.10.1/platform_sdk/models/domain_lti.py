from dataclasses import dataclass

@dataclass
class DomainLTI:
    domain: int
    lti: int
    key: str
    secret: str
    is_disabled: bool
    domain_name: str
    lti_title: str


@dataclass
class DomainLTIExtended:
    key: str
    secret: str
    is_disabled: bool
    domain: int
    domain_name: str
    lti: int
    lti_title: str
    lti_identifier: str
    lti_is_disabled: bool
