import datetime
import typing

import kubernetes.client

class V1beta2StatefulSet:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta2StatefulSetSpec]
    status: typing.Optional[kubernetes.client.V1beta2StatefulSetStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta2StatefulSetSpec] = ..., status: typing.Optional[kubernetes.client.V1beta2StatefulSetStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2StatefulSetDict:
        ...
class V1beta2StatefulSetDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta2StatefulSetSpecDict]
    status: typing.Optional[kubernetes.client.V1beta2StatefulSetStatusDict]
