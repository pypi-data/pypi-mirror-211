import datetime
import typing

import kubernetes.client

class V1beta1PriorityClass:
    api_version: typing.Optional[str]
    description: typing.Optional[str]
    global_default: typing.Optional[bool]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    value: int
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., description: typing.Optional[str] = ..., global_default: typing.Optional[bool] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., value: int) -> None:
        ...
    def to_dict(self) -> V1beta1PriorityClassDict:
        ...
class V1beta1PriorityClassDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    description: typing.Optional[str]
    globalDefault: typing.Optional[bool]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    value: int
