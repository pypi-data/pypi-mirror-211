import datetime
import typing

import kubernetes.client

class PolicyV1beta1AllowedFlexVolume:
    driver: str
    
    def __init__(self, *, driver: str) -> None:
        ...
    def to_dict(self) -> PolicyV1beta1AllowedFlexVolumeDict:
        ...
class PolicyV1beta1AllowedFlexVolumeDict(typing.TypedDict, total=False):
    driver: str
