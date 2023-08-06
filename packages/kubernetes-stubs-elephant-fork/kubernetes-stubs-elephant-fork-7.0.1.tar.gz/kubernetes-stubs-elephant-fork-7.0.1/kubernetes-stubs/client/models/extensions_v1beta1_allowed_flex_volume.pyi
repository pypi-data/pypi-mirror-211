import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1AllowedFlexVolume:
    driver: str
    
    def __init__(self, *, driver: str) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1AllowedFlexVolumeDict:
        ...
class ExtensionsV1beta1AllowedFlexVolumeDict(typing.TypedDict, total=False):
    driver: str
