import datetime
import typing

import kubernetes.client

class PolicyV1beta1SupplementalGroupsStrategyOptions:
    ranges: typing.Optional[list[kubernetes.client.PolicyV1beta1IDRange]]
    rule: typing.Optional[str]
    
    def __init__(self, *, ranges: typing.Optional[list[kubernetes.client.PolicyV1beta1IDRange]] = ..., rule: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> PolicyV1beta1SupplementalGroupsStrategyOptionsDict:
        ...
class PolicyV1beta1SupplementalGroupsStrategyOptionsDict(typing.TypedDict, total=False):
    ranges: typing.Optional[list[kubernetes.client.PolicyV1beta1IDRangeDict]]
    rule: typing.Optional[str]
