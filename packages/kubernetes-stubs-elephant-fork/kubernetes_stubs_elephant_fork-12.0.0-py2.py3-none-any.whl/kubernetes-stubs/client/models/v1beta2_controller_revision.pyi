import datetime
import typing

import kubernetes.client

class V1beta2ControllerRevision:
    api_version: typing.Optional[str]
    data: typing.Optional[typing.Any]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    revision: int
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., data: typing.Optional[typing.Any] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., revision: int) -> None:
        ...
    def to_dict(self) -> V1beta2ControllerRevisionDict:
        ...
class V1beta2ControllerRevisionDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    data: typing.Optional[typing.Any]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    revision: int
