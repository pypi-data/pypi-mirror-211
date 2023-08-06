import datetime
import typing

import kubernetes.client

class V1PodSecurityContext:
    fs_group: typing.Optional[int]
    run_as_group: typing.Optional[int]
    run_as_non_root: typing.Optional[bool]
    run_as_user: typing.Optional[int]
    se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions]
    supplemental_groups: typing.Optional[list[int]]
    sysctls: typing.Optional[list[kubernetes.client.V1Sysctl]]
    
    def __init__(self, *, fs_group: typing.Optional[int] = ..., run_as_group: typing.Optional[int] = ..., run_as_non_root: typing.Optional[bool] = ..., run_as_user: typing.Optional[int] = ..., se_linux_options: typing.Optional[kubernetes.client.V1SELinuxOptions] = ..., supplemental_groups: typing.Optional[list[int]] = ..., sysctls: typing.Optional[list[kubernetes.client.V1Sysctl]] = ...) -> None:
        ...
    def to_dict(self) -> V1PodSecurityContextDict:
        ...
class V1PodSecurityContextDict(typing.TypedDict, total=False):
    fsGroup: typing.Optional[int]
    runAsGroup: typing.Optional[int]
    runAsNonRoot: typing.Optional[bool]
    runAsUser: typing.Optional[int]
    seLinuxOptions: typing.Optional[kubernetes.client.V1SELinuxOptionsDict]
    supplementalGroups: typing.Optional[list[int]]
    sysctls: typing.Optional[list[kubernetes.client.V1SysctlDict]]
