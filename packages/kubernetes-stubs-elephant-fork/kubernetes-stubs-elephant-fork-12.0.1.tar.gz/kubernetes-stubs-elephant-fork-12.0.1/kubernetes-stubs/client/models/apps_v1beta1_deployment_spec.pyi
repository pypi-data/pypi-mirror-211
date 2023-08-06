import datetime
import typing

import kubernetes.client

class AppsV1beta1DeploymentSpec:
    min_ready_seconds: typing.Optional[int]
    paused: typing.Optional[bool]
    progress_deadline_seconds: typing.Optional[int]
    replicas: typing.Optional[int]
    revision_history_limit: typing.Optional[int]
    rollback_to: typing.Optional[kubernetes.client.AppsV1beta1RollbackConfig]
    selector: typing.Optional[kubernetes.client.V1LabelSelector]
    strategy: typing.Optional[kubernetes.client.AppsV1beta1DeploymentStrategy]
    template: kubernetes.client.V1PodTemplateSpec
    
    def __init__(self, *, min_ready_seconds: typing.Optional[int] = ..., paused: typing.Optional[bool] = ..., progress_deadline_seconds: typing.Optional[int] = ..., replicas: typing.Optional[int] = ..., revision_history_limit: typing.Optional[int] = ..., rollback_to: typing.Optional[kubernetes.client.AppsV1beta1RollbackConfig] = ..., selector: typing.Optional[kubernetes.client.V1LabelSelector] = ..., strategy: typing.Optional[kubernetes.client.AppsV1beta1DeploymentStrategy] = ..., template: kubernetes.client.V1PodTemplateSpec) -> None:
        ...
    def to_dict(self) -> AppsV1beta1DeploymentSpecDict:
        ...
class AppsV1beta1DeploymentSpecDict(typing.TypedDict, total=False):
    minReadySeconds: typing.Optional[int]
    paused: typing.Optional[bool]
    progressDeadlineSeconds: typing.Optional[int]
    replicas: typing.Optional[int]
    revisionHistoryLimit: typing.Optional[int]
    rollbackTo: typing.Optional[kubernetes.client.AppsV1beta1RollbackConfigDict]
    selector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    strategy: typing.Optional[kubernetes.client.AppsV1beta1DeploymentStrategyDict]
    template: kubernetes.client.V1PodTemplateSpecDict
