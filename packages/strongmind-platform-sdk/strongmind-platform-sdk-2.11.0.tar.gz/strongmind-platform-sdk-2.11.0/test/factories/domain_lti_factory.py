from factory import Factory, Faker

from platform_sdk.models.domain_lti import DomainLTI


class DomainLTIFactory(Factory):
    class Meta:
        model = DomainLTI

    key = Faker('word')
    secret = Faker('word')
    is_disabled = False
    domain = Faker('random_int')
    domain_name = Faker('domain_name')
    lti = Faker('random_int')
    lti_title = Faker('word')
    lti_identifier = Faker('word')
    lti_is_disabled = False
