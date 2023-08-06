import datetime
import typing

import kubernetes.client

class V1alpha1EndpointSlice:
    address_type: typing.Optional[str]
    api_version: typing.Optional[str]
    endpoints: list[kubernetes.client.V1alpha1Endpoint]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    ports: typing.Optional[list[kubernetes.client.V1alpha1EndpointPort]]
    
    def __init__(self, *, address_type: typing.Optional[str] = ..., api_version: typing.Optional[str] = ..., endpoints: list[kubernetes.client.V1alpha1Endpoint], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., ports: typing.Optional[list[kubernetes.client.V1alpha1EndpointPort]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EndpointSliceDict:
        ...
class V1alpha1EndpointSliceDict(typing.TypedDict, total=False):
    addressType: typing.Optional[str]
    apiVersion: typing.Optional[str]
    endpoints: list[kubernetes.client.V1alpha1EndpointDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    ports: typing.Optional[list[kubernetes.client.V1alpha1EndpointPortDict]]
