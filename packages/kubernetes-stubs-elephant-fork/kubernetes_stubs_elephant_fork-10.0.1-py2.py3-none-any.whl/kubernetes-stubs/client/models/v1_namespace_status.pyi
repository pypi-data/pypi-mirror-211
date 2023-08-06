import datetime
import typing

import kubernetes.client

class V1NamespaceStatus:
    phase: typing.Optional[str]
    
    def __init__(self, *, phase: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1NamespaceStatusDict:
        ...
class V1NamespaceStatusDict(typing.TypedDict, total=False):
    phase: typing.Optional[str]
