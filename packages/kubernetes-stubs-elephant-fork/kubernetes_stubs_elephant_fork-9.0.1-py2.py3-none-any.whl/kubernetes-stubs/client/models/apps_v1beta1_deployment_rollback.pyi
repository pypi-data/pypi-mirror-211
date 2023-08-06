import datetime
import typing

import kubernetes.client

class AppsV1beta1DeploymentRollback:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    name: str
    rollback_to: kubernetes.client.AppsV1beta1RollbackConfig
    updated_annotations: typing.Optional[dict[str, str]]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., name: str, rollback_to: kubernetes.client.AppsV1beta1RollbackConfig, updated_annotations: typing.Optional[dict[str, str]] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1DeploymentRollbackDict:
        ...
class AppsV1beta1DeploymentRollbackDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    name: str
    rollbackTo: kubernetes.client.AppsV1beta1RollbackConfigDict
    updatedAnnotations: typing.Optional[dict[str, str]]
