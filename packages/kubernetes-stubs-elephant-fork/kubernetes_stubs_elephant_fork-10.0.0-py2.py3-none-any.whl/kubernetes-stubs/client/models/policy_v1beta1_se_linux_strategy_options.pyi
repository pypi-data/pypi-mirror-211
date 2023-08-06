import datetime
import typing

import kubernetes.client

class PolicyV1beta1SELinuxStrategyOptions:
    rule: str
    se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions]
    
    def __init__(self, *, rule: str, se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions] = ...) -> None:
        ...
    def to_dict(self) -> PolicyV1beta1SELinuxStrategyOptionsDict:
        ...
class PolicyV1beta1SELinuxStrategyOptionsDict(typing.TypedDict, total=False):
    rule: str
    seLinuxOptions: typing.Optional[kubernetes.client.V1SELinuxOptionsDict]
