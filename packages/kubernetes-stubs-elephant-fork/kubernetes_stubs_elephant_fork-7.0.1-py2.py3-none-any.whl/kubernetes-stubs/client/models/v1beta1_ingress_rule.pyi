import datetime
import typing

import kubernetes.client

class V1beta1IngressRule:
    host: typing.Optional[str]
    http: typing.Optional[kubernetes.client.V1beta1HTTPIngressRuleValue]
    
    def __init__(self, *, host: typing.Optional[str] = ..., http: typing.Optional[kubernetes.client.V1beta1HTTPIngressRuleValue] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1IngressRuleDict:
        ...
class V1beta1IngressRuleDict(typing.TypedDict, total=False):
    host: typing.Optional[str]
    http: typing.Optional[kubernetes.client.V1beta1HTTPIngressRuleValueDict]
