import datetime
import typing

import kubernetes.client

class V1beta1IngressSpec:
    backend: typing.Optional[kubernetes.client.V1beta1IngressBackend]
    rules: typing.Optional[list[kubernetes.client.V1beta1IngressRule]]
    tls: typing.Optional[list[kubernetes.client.V1beta1IngressTLS]]
    
    def __init__(self, *, backend: typing.Optional[kubernetes.client.V1beta1IngressBackend] = ..., rules: typing.Optional[list[kubernetes.client.V1beta1IngressRule]] = ..., tls: typing.Optional[list[kubernetes.client.V1beta1IngressTLS]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1IngressSpecDict:
        ...
class V1beta1IngressSpecDict(typing.TypedDict, total=False):
    backend: typing.Optional[kubernetes.client.V1beta1IngressBackendDict]
    rules: typing.Optional[list[kubernetes.client.V1beta1IngressRuleDict]]
    tls: typing.Optional[list[kubernetes.client.V1beta1IngressTLSDict]]
