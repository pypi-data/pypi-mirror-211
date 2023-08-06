import datetime
import typing

import kubernetes.client

class AppsV1beta1DeploymentList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.AppsV1beta1Deployment]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.AppsV1beta1Deployment], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1DeploymentListDict:
        ...
class AppsV1beta1DeploymentListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.AppsV1beta1DeploymentDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
