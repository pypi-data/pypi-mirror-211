import datetime
import typing

import kubernetes.client

class V1alpha1EndpointPort:
    name: typing.Optional[str]
    port: typing.Optional[int]
    protocol: typing.Optional[str]
    
    def __init__(self, *, name: typing.Optional[str] = ..., port: typing.Optional[int] = ..., protocol: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EndpointPortDict:
        ...
class V1alpha1EndpointPortDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
    port: typing.Optional[int]
    protocol: typing.Optional[str]
