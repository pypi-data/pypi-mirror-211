import datetime
import typing

import kubernetes.client

class V1beta1StatefulSetSpec:
    pod_management_policy: typing.Optional[str]
    replicas: typing.Optional[int]
    revision_history_limit: typing.Optional[int]
    selector: typing.Optional[kubernetes.client.V1LabelSelector]
    service_name: str
    template: kubernetes.client.V1PodTemplateSpec
    update_strategy: typing.Optional[kubernetes.client.V1beta1StatefulSetUpdateStrategy]
    volume_claim_templates: typing.Optional[list[kubernetes.client.V1PersistentVolumeClaim]]
    
    def __init__(self, *, pod_management_policy: typing.Optional[str] = ..., replicas: typing.Optional[int] = ..., revision_history_limit: typing.Optional[int] = ..., selector: typing.Optional[kubernetes.client.V1LabelSelector] = ..., service_name: str, template: kubernetes.client.V1PodTemplateSpec, update_strategy: typing.Optional[kubernetes.client.V1beta1StatefulSetUpdateStrategy] = ..., volume_claim_templates: typing.Optional[list[kubernetes.client.V1PersistentVolumeClaim]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1StatefulSetSpecDict:
        ...
class V1beta1StatefulSetSpecDict(typing.TypedDict, total=False):
    podManagementPolicy: typing.Optional[str]
    replicas: typing.Optional[int]
    revisionHistoryLimit: typing.Optional[int]
    selector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    serviceName: str
    template: kubernetes.client.V1PodTemplateSpecDict
    updateStrategy: typing.Optional[kubernetes.client.V1beta1StatefulSetUpdateStrategyDict]
    volumeClaimTemplates: typing.Optional[list[kubernetes.client.V1PersistentVolumeClaimDict]]
