import datetime
import typing

import kubernetes.client

class V1beta1Webhook:
    client_config: kubernetes.client.V1beta1WebhookClientConfig
    failure_policy: typing.Optional[str]
    name: str
    namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    rules: typing.Optional[list[kubernetes.client.V1beta1RuleWithOperations]]
    side_effects: typing.Optional[str]
    
    def __init__(self, *, client_config: kubernetes.client.V1beta1WebhookClientConfig, failure_policy: typing.Optional[str] = ..., name: str, namespace_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ..., rules: typing.Optional[list[kubernetes.client.V1beta1RuleWithOperations]] = ..., side_effects: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1WebhookDict:
        ...
class V1beta1WebhookDict(typing.TypedDict, total=False):
    clientConfig: kubernetes.client.V1beta1WebhookClientConfigDict
    failurePolicy: typing.Optional[str]
    name: str
    namespaceSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    rules: typing.Optional[list[kubernetes.client.V1beta1RuleWithOperationsDict]]
    sideEffects: typing.Optional[str]
