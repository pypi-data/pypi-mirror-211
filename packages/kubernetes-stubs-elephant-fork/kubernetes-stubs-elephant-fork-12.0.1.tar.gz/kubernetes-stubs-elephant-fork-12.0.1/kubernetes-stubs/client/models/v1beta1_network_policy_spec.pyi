import datetime
import typing

import kubernetes.client

class V1beta1NetworkPolicySpec:
    egress: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyEgressRule]]
    ingress: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyIngressRule]]
    pod_selector: kubernetes.client.V1LabelSelector
    policy_types: typing.Optional[list[str]]
    
    def __init__(self, *, egress: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyEgressRule]] = ..., ingress: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyIngressRule]] = ..., pod_selector: kubernetes.client.V1LabelSelector, policy_types: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1NetworkPolicySpecDict:
        ...
class V1beta1NetworkPolicySpecDict(typing.TypedDict, total=False):
    egress: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyEgressRuleDict]]
    ingress: typing.Optional[list[kubernetes.client.V1beta1NetworkPolicyIngressRuleDict]]
    podSelector: kubernetes.client.V1LabelSelectorDict
    policyTypes: typing.Optional[list[str]]
