import aws_cdk as cdk
from constructs import Construct

import attrs


@attrs.define
class Infrastructure:

    scope: cdk.Stack
    id: str = attrs.field(converter=str, validator=attrs.validators.instance_of(str))

    @property
    def kwargs(self):
        return attrs.asdict(self)

    def build(self, **kwargs) -> Construct:
        raise NotImplementedError(f'{self.__class__} must be implemented')
