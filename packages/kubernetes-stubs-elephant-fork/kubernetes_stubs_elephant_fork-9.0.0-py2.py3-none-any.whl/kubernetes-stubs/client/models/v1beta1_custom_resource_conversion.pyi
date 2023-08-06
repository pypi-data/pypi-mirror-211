import datetime
import typing

import kubernetes.client

class V1beta1CustomResourceConversion:
    strategy: str
    webhook_client_config: typing.Optional[kubernetes.client.ApiextensionsV1beta1WebhookClientConfig]
    
    def __init__(self, *, strategy: str, webhook_client_config: typing.Optional[kubernetes.client.ApiextensionsV1beta1WebhookClientConfig] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CustomResourceConversionDict:
        ...
class V1beta1CustomResourceConversionDict(typing.TypedDict, total=False):
    strategy: str
    webhookClientConfig: typing.Optional[kubernetes.client.ApiextensionsV1beta1WebhookClientConfigDict]
