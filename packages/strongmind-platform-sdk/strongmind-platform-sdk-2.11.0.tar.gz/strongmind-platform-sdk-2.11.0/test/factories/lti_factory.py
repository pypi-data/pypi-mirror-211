from factory import Factory, Faker

from platform_sdk.models.lti import Lti


class LtiFactory(Factory):
    class Meta:
        model = Lti

    id = Faker('random_int')
    title = Faker('word')
    identifier = Faker('word')
    is_disabled = False
