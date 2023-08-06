from __future__ import annotations

from typing import Dict, List, Optional

from aws_cdk import aws_ec2 as ec2

import attrs
from attrs import validators

from cdk_blueprint import Infrastructure


def validate_max_azs(instance: Vpc, attributes: attrs.field, value: int) -> None:
    if value < 0:
        raise ValueError('max_az must be greater or equal to 0')
    total = len(instance.scope.availability_zones)
    if value > total:
        raise ValueError(f'max_az must be less than or equal to {total}')


@attrs.define
class Vpc(Infrastructure):
    """
    https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ec2/Vpc.html#vpc
    """
    cidr: Optional[str] = attrs.field(default=ec2.Vpc.DEFAULT_CIDR_RANGE)
    max_azs: Optional[int] = attrs.field(default=1, converter=int, validator=validate_max_azs)
    subnet_configuration: Optional[List[Dict]] = attrs.field(
        factory=list,
        validator=validators.optional(
            validators.deep_iterable(
                member_validator=validators.instance_of(dict)
            )
        )
    )

    def build(self, **kwargs) -> ec2.Vpc:
        for key, val in kwargs.items():
            setattr(self, key, val)
        return ec2.Vpc(**self.kwargs)

    def from_lookup(self, vpc_id: str) -> ec2.Vpc:
        return ec2.Vpc.from_lookup(self.scope, self.id, vpc_id=vpc_id)
