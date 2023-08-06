import datetime
import typing

import kubernetes.client

class V2beta1PodsMetricSource:
    metric_name: str
    target_average_value: str
    
    def __init__(self, *, metric_name: str, target_average_value: str) -> None:
        ...
    def to_dict(self) -> V2beta1PodsMetricSourceDict:
        ...
class V2beta1PodsMetricSourceDict(typing.TypedDict, total=False):
    metricName: str
    targetAverageValue: str
