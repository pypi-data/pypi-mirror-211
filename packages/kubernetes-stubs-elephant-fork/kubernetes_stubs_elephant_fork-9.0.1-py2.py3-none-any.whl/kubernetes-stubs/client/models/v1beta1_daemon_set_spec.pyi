import datetime
import typing

import kubernetes.client

class V1beta1DaemonSetSpec:
    min_ready_seconds: typing.Optional[int]
    revision_history_limit: typing.Optional[int]
    selector: typing.Optional[kubernetes.client.V1LabelSelector]
    template: kubernetes.client.V1PodTemplateSpec
    template_generation: typing.Optional[int]
    update_strategy: typing.Optional[kubernetes.client.V1beta1DaemonSetUpdateStrategy]
    
    def __init__(self, *, min_ready_seconds: typing.Optional[int] = ..., revision_history_limit: typing.Optional[int] = ..., selector: typing.Optional[kubernetes.client.V1LabelSelector] = ..., template: kubernetes.client.V1PodTemplateSpec, template_generation: typing.Optional[int] = ..., update_strategy: typing.Optional[kubernetes.client.V1beta1DaemonSetUpdateStrategy] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DaemonSetSpecDict:
        ...
class V1beta1DaemonSetSpecDict(typing.TypedDict, total=False):
    minReadySeconds: typing.Optional[int]
    revisionHistoryLimit: typing.Optional[int]
    selector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    template: kubernetes.client.V1PodTemplateSpecDict
    templateGeneration: typing.Optional[int]
    updateStrategy: typing.Optional[kubernetes.client.V1beta1DaemonSetUpdateStrategyDict]
