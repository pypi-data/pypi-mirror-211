import datetime
import typing

import kubernetes.client

class V1beta1HTTPIngressRuleValue:
    paths: list[kubernetes.client.V1beta1HTTPIngressPath]
    
    def __init__(self, *, paths: list[kubernetes.client.V1beta1HTTPIngressPath]) -> None:
        ...
    def to_dict(self) -> V1beta1HTTPIngressRuleValueDict:
        ...
class V1beta1HTTPIngressRuleValueDict(typing.TypedDict, total=False):
    paths: list[kubernetes.client.V1beta1HTTPIngressPathDict]
