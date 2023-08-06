import datetime
import typing

import kubernetes.client

class V1ServiceReference:
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    
    def __init__(self, *, name: typing.Optional[str] = ..., namespace: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1ServiceReferenceDict:
        ...
class V1ServiceReferenceDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
    namespace: typing.Optional[str]
