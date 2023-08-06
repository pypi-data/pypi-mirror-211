import datetime
import typing

import kubernetes.client

class V1beta1NetworkPolicyPeer:
    ip_block: typing.Optional[kubernetes.client.V1beta1IPBlock]
    namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    pod_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    
    def __init__(self, *, ip_block: typing.Optional[kubernetes.client.V1beta1IPBlock] = ..., namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ..., pod_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1NetworkPolicyPeerDict:
        ...
class V1beta1NetworkPolicyPeerDict(typing.TypedDict, total=False):
    ipBlock: typing.Optional[kubernetes.client.V1beta1IPBlockDict]
    namespaceSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    podSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
