import datetime
import typing

import kubernetes.client

class V1alpha1Endpoint:
    addresses: list[str]
    conditions: typing.Optional[kubernetes.client.V1alpha1EndpointConditions]
    hostname: typing.Optional[str]
    target_ref: typing.Optional[kubernetes.client.V1ObjectReference]
    topology: typing.Optional[dict[str, str]]
    
    def __init__(self, *, addresses: list[str], conditions: typing.Optional[kubernetes.client.V1alpha1EndpointConditions] = ..., hostname: typing.Optional[str] = ..., target_ref: typing.Optional[kubernetes.client.V1ObjectReference] = ..., topology: typing.Optional[dict[str, str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EndpointDict:
        ...
class V1alpha1EndpointDict(typing.TypedDict, total=False):
    addresses: list[str]
    conditions: typing.Optional[kubernetes.client.V1alpha1EndpointConditionsDict]
    hostname: typing.Optional[str]
    targetRef: typing.Optional[kubernetes.client.V1ObjectReferenceDict]
    topology: typing.Optional[dict[str, str]]
