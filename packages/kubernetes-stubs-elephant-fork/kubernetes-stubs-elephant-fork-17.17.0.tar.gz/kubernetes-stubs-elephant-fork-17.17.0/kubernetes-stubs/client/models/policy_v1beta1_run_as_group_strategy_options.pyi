import datetime
import typing

import kubernetes.client

class PolicyV1beta1RunAsGroupStrategyOptions:
    ranges: typing.Optional[list[kubernetes.client.PolicyV1beta1IDRange]]
    rule: str
    
    def __init__(self, *, ranges: typing.Optional[list[kubernetes.client.PolicyV1beta1IDRange]] = ..., rule: str) -> None:
        ...
    def to_dict(self) -> PolicyV1beta1RunAsGroupStrategyOptionsDict:
        ...
class PolicyV1beta1RunAsGroupStrategyOptionsDict(typing.TypedDict, total=False):
    ranges: typing.Optional[list[kubernetes.client.PolicyV1beta1IDRangeDict]]
    rule: str
