import datetime
import typing

import kubernetes.client

class AppsV1beta1Deployment:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.AppsV1beta1DeploymentSpec]
    status: typing.Optional[kubernetes.client.AppsV1beta1DeploymentStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.AppsV1beta1DeploymentSpec] = ..., status: typing.Optional[kubernetes.client.AppsV1beta1DeploymentStatus] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1DeploymentDict:
        ...
class AppsV1beta1DeploymentDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.AppsV1beta1DeploymentSpecDict]
    status: typing.Optional[kubernetes.client.AppsV1beta1DeploymentStatusDict]
