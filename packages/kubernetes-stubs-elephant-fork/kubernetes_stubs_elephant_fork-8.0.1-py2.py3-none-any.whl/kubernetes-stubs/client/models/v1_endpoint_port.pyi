import datetime
import typing

import kubernetes.client

class V1EndpointPort:
    name: typing.Optional[str]
    port: int
    protocol: typing.Optional[str]
    
    def __init__(self, *, name: typing.Optional[str] = ..., port: int, protocol: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1EndpointPortDict:
        ...
class V1EndpointPortDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
    port: int
    protocol: typing.Optional[str]
