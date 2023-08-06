import datetime
import typing

import kubernetes.client

class V1alpha1EndpointSliceList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1EndpointSlice]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1alpha1EndpointSlice], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EndpointSliceListDict:
        ...
class V1alpha1EndpointSliceListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1EndpointSliceDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
