import datetime
import typing

import kubernetes.client

class V1LocalVolumeSource:
    path: str
    
    def __init__(self, *, path: str) -> None:
        ...
    def to_dict(self) -> V1LocalVolumeSourceDict:
        ...
class V1LocalVolumeSourceDict(typing.TypedDict, total=False):
    path: str
