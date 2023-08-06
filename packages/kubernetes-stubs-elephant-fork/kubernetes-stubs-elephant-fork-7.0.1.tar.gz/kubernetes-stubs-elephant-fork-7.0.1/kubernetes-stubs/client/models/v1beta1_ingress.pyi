import datetime
import typing

import kubernetes.client

class V1beta1Ingress:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta1IngressSpec]
    status: typing.Optional[kubernetes.client.V1beta1IngressStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta1IngressSpec] = ..., status: typing.Optional[kubernetes.client.V1beta1IngressStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1IngressDict:
        ...
class V1beta1IngressDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta1IngressSpecDict]
    status: typing.Optional[kubernetes.client.V1beta1IngressStatusDict]
