from factory import Factory, Faker

from platform_sdk.models.domain_lti import DomainLTI, DomainLTIExtended


class DomainLTIFactory(Factory):
    class Meta:
        model = DomainLTI

    domain = Faker('random_int')
    lti = Faker('random_int')
    key = Faker('word')
    secret = Faker('word')
    is_disabled = False
    domain_name = Faker('domain_name')
    lti_title = Faker('word')


class DomainLTIExtendedFactory(Factory):
    class Meta:
        model = DomainLTIExtended

    domain = Faker('random_int')
    lti = Faker('random_int')
    key = Faker('word')
    secret = Faker('word')
    is_disabled = False
    domain_name = Faker('domain_name')
    lti_title = Faker('word')
    lti_identifier = Faker('word')
    lti_is_disabled = False
