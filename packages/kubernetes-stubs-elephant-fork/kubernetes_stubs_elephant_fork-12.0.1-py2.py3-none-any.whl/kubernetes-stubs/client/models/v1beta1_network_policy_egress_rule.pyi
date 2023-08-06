import datetime
import typing

import kubernetes.client

class V1beta1NetworkPolicyEgressRule:
    ports: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPort]]
    to: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPeer]]
    
    def __init__(self, *, ports: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPort]] = ..., to: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPeer]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1NetworkPolicyEgressRuleDict:
        ...
class V1beta1NetworkPolicyEgressRuleDict(typing.TypedDict, total=False):
    ports: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPortDict]]
    to: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyPeerDict]]
