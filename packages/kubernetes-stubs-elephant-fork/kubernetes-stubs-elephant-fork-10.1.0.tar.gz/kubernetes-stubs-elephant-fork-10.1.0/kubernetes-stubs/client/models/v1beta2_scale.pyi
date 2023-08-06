import datetime
import typing

import kubernetes.client

class V1beta2Scale:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta2ScaleSpec]
    status: typing.Optional[kubernetes.client.V1beta2ScaleStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta2ScaleSpec] = ..., status: typing.Optional[kubernetes.client.V1beta2ScaleStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2ScaleDict:
        ...
class V1beta2ScaleDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta2ScaleSpecDict]
    status: typing.Optional[kubernetes.client.V1beta2ScaleStatusDict]
