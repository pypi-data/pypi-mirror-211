import datetime
import typing

import kubernetes.client

class AppsV1beta1Scale:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.AppsV1beta1ScaleSpec]
    status: typing.Optional[kubernetes.client.AppsV1beta1ScaleStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.AppsV1beta1ScaleSpec] = ..., status: typing.Optional[kubernetes.client.AppsV1beta1ScaleStatus] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1ScaleDict:
        ...
class AppsV1beta1ScaleDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.AppsV1beta1ScaleSpecDict]
    status: typing.Optional[kubernetes.client.AppsV1beta1ScaleStatusDict]
