import datetime
import typing

import kubernetes.client

class V1beta1HTTPIngressPath:
    backend: kubernetes.client.V1beta1IngressBackend
    path: typing.Optional[str]
    
    def __init__(self, *, backend: kubernetes.client.V1beta1IngressBackend, path: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1HTTPIngressPathDict:
        ...
class V1beta1HTTPIngressPathDict(typing.TypedDict, total=False):
    backend: kubernetes.client.V1beta1IngressBackendDict
    path: typing.Optional[str]
