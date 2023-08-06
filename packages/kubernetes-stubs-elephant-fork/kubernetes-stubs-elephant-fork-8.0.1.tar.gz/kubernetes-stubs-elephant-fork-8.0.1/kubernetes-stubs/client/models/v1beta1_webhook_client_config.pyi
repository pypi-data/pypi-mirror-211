import datetime
import typing

import kubernetes.client

class V1beta1WebhookClientConfig:
    ca_bundle: str
    service: typing.Optional[kubernetes.client.AdmissionregistrationV1beta1ServiceReference]
    url: typing.Optional[str]
    
    def __init__(self, *, ca_bundle: str, service: typing.Optional[kubernetes.client.AdmissionregistrationV1beta1ServiceReference] = ..., url: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1WebhookClientConfigDict:
        ...
class V1beta1WebhookClientConfigDict(typing.TypedDict, total=False):
    caBundle: str
    service: typing.Optional[kubernetes.client.AdmissionregistrationV1beta1ServiceReferenceDict]
    url: typing.Optional[str]
