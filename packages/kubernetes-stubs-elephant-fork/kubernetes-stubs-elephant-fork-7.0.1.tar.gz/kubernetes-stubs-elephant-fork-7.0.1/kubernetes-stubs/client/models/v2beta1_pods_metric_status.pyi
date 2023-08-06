import datetime
import typing

import kubernetes.client

class V2beta1PodsMetricStatus:
    current_average_value: str
    metric_name: str
    
    def __init__(self, *, current_average_value: str, metric_name: str) -> None:
        ...
    def to_dict(self) -> V2beta1PodsMetricStatusDict:
        ...
class V2beta1PodsMetricStatusDict(typing.TypedDict, total=False):
    currentAverageValue: str
    metricName: str
