import datetime
import typing

import kubernetes.client

class V1beta2StatefulSetList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1beta2StatefulSet]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1beta2StatefulSet], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2StatefulSetListDict:
        ...
class V1beta2StatefulSetListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1beta2StatefulSetDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
