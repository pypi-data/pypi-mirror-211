import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1RunAsUserStrategyOptions:
    ranges: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IDRange]]
    rule: str
    
    def __init__(self, *, ranges: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IDRange]] = ..., rule: str) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1RunAsUserStrategyOptionsDict:
        ...
class ExtensionsV1beta1RunAsUserStrategyOptionsDict(typing.TypedDict, total=False):
    ranges: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IDRangeDict]]
    rule: str
