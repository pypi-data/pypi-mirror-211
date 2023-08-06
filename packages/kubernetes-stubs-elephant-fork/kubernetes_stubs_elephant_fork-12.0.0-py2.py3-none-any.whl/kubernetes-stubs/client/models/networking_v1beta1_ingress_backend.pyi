import datetime
import typing

import kubernetes.client

class NetworkingV1beta1IngressBackend:
    service_name: str
    service_port: typing.Any
    
    def __init__(self, *, service_name: str, service_port: typing.Any) -> None:
        ...
    def to_dict(self) -> NetworkingV1beta1IngressBackendDict:
        ...
class NetworkingV1beta1IngressBackendDict(typing.TypedDict, total=False):
    serviceName: str
    servicePort: typing.Any
