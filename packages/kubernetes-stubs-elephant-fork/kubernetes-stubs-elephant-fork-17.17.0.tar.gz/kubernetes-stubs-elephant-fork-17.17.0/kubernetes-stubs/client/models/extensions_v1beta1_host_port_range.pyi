import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1HostPortRange:
    max: int
    min: int
    
    def __init__(self, *, max: int, min: int) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1HostPortRangeDict:
        ...
class ExtensionsV1beta1HostPortRangeDict(typing.TypedDict, total=False):
    max: int
    min: int
