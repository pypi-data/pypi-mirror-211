import datetime
import typing

import kubernetes.client

class V1Initializers:
    pending: list[kubernetes.client.V1Initializer]
    result: typing.Optional[kubernetes.client.V1Status]
    
    def __init__(self, *, pending: list[kubernetes.client.V1Initializer], result: typing.Optional[kubernetes.client.V1Status] = ...) -> None:
        ...
    def to_dict(self) -> V1InitializersDict:
        ...
class V1InitializersDict(typing.TypedDict, total=False):
    pending: list[kubernetes.client.V1InitializerDict]
    result: typing.Optional[kubernetes.client.V1StatusDict]
