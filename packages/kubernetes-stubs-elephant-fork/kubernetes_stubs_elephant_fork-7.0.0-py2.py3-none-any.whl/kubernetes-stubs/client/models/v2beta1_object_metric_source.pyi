import datetime
import typing

import kubernetes.client

class V2beta1ObjectMetricSource:
    metric_name: str
    target: kubernetes.client.V2beta1CrossVersionObjectReference
    target_value: str
    
    def __init__(self, *, metric_name: str, target: kubernetes.client.V2beta1CrossVersionObjectReference, target_value: str) -> None:
        ...
    def to_dict(self) -> V2beta1ObjectMetricSourceDict:
        ...
class V2beta1ObjectMetricSourceDict(typing.TypedDict, total=False):
    metricName: str
    target: kubernetes.client.V2beta1CrossVersionObjectReferenceDict
    targetValue: str
