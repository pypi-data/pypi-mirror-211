import datetime
import typing

import kubernetes.client

class V1alpha1InitializerConfiguration:
    api_version: typing.Optional[str]
    initializers: typing.Optional[list[kubernetes.client.V1alpha1Initializer]]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., initializers: typing.Optional[list[kubernetes.client.V1alpha1Initializer]] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1InitializerConfigurationDict:
        ...
class V1alpha1InitializerConfigurationDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    initializers: typing.Optional[list[kubernetes.client.V1alpha1InitializerDict]]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
