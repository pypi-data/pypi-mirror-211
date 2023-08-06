import datetime
import typing

import kubernetes.client

class V2beta1ObjectMetricStatus:
    current_value: str
    metric_name: str
    target: kubernetes.client.V2beta1CrossVersionObjectReference
    
    def __init__(self, *, current_value: str, metric_name: str, target: kubernetes.client.V2beta1CrossVersionObjectReference) -> None:
        ...
    def to_dict(self) -> V2beta1ObjectMetricStatusDict:
        ...
class V2beta1ObjectMetricStatusDict(typing.TypedDict, total=False):
    currentValue: str
    metricName: str
    target: kubernetes.client.V2beta1CrossVersionObjectReferenceDict
