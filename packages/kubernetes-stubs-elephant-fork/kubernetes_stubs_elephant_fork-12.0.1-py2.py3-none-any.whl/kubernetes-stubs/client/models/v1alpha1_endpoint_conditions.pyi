import datetime
import typing

import kubernetes.client

class V1alpha1EndpointConditions:
    ready: typing.Optional[bool]
    
    def __init__(self, *, ready: typing.Optional[bool] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EndpointConditionsDict:
        ...
class V1alpha1EndpointConditionsDict(typing.TypedDict, total=False):
    ready: typing.Optional[bool]
