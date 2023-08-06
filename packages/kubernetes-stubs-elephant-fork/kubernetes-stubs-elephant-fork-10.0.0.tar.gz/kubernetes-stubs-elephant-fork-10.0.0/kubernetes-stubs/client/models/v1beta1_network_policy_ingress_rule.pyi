import datetime
import typing

import kubernetes.client

class V1beta1NetworkPolicyIngressRule:
    _from: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPeer]]
    ports: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPort]]
    
    def __init__(self, *, _from: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPeer]] = ..., ports: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPort]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1NetworkPolicyIngressRuleDict:
        ...
class V1beta1NetworkPolicyIngressRuleDict(typing.TypedDict, total=False):
    _from: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPeerDict]]
    ports: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPortDict]]
