import datetime
import typing

import kubernetes.client

class V1beta1VolumeAttachmentSource:
    persistent_volume_name: typing.Optional[str]
    
    def __init__(self, *, persistent_volume_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1VolumeAttachmentSourceDict:
        ...
class V1beta1VolumeAttachmentSourceDict(typing.TypedDict, total=False):
    persistentVolumeName: typing.Optional[str]
