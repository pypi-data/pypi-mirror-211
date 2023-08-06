import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1RuntimeClassStrategyOptions:
    allowed_runtime_class_names: list[str]
    default_runtime_class_name: typing.Optional[str]
    
    def __init__(self, *, allowed_runtime_class_names: list[str], default_runtime_class_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1RuntimeClassStrategyOptionsDict:
        ...
class ExtensionsV1beta1RuntimeClassStrategyOptionsDict(typing.TypedDict, total=False):
    allowedRuntimeClassNames: list[str]
    defaultRuntimeClassName: typing.Optional[str]
