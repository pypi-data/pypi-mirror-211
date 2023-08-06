import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1SupplementalGroupsStrategyOptions:
    ranges: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IDRange]]
    rule: typing.Optional[str]
    
    def __init__(self, *, ranges: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IDRange]] = ..., rule: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1SupplementalGroupsStrategyOptionsDict:
        ...
class ExtensionsV1beta1SupplementalGroupsStrategyOptionsDict(typing.TypedDict, total=False):
    ranges: typing.Optional[list[kubernetes.client.ExtensionsV1beta1IDRangeDict]]
    rule: typing.Optional[str]
