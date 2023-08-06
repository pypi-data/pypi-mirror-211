import datetime
import typing

import kubernetes.client

class V1Preconditions:
    uid: typing.Optional[str]
    
    def __init__(self, *, uid: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1PreconditionsDict:
        ...
class V1PreconditionsDict(typing.TypedDict, total=False):
    uid: typing.Optional[str]
