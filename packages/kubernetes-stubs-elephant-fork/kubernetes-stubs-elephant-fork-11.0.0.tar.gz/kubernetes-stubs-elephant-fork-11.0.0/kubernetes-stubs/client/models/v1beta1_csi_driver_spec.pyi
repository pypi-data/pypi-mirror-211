import datetime
import typing

import kubernetes.client

class V1beta1CSIDriverSpec:
    attach_required: typing.Optional[bool]
    pod_info_on_mount: typing.Optional[bool]
    
    def __init__(self, *, attach_required: typing.Optional[bool] = ..., pod_info_on_mount: typing.Optional[bool] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CSIDriverSpecDict:
        ...
class V1beta1CSIDriverSpecDict(typing.TypedDict, total=False):
    attachRequired: typing.Optional[bool]
    podInfoOnMount: typing.Optional[bool]
