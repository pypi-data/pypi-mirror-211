import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1PodSecurityPolicySpec:
    allow_privilege_escalation: typing.Optional[bool]
    allowed_csi_drivers: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedCSIDriver]]
    allowed_capabilities: typing.Optional[list[str]]
    allowed_flex_volumes: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedFlexVolume]]
    allowed_host_paths: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedHostPath]]
    allowed_proc_mount_types: typing.Optional[list[str]]
    allowed_unsafe_sysctls: typing.Optional[list[str]]
    default_add_capabilities: typing.Optional[list[str]]
    default_allow_privilege_escalation: typing.Optional[bool]
    forbidden_sysctls: typing.Optional[list[str]]
    fs_group: kubernetes.client.ExtensionsV1beta1FSGroupStrategyOptions
    host_ipc: typing.Optional[bool]
    host_network: typing.Optional[bool]
    host_pid: typing.Optional[bool]
    host_ports: typing.Optional[list[kubernetes.client.ExtensionsV1beta1HostPortRange]]
    privileged: typing.Optional[bool]
    read_only_root_filesystem: typing.Optional[bool]
    required_drop_capabilities: typing.Optional[list[str]]
    run_as_group: typing.Optional[kubernetes.client.ExtensionsV1beta1RunAsGroupStrategyOptions]
    run_as_user: kubernetes.client.ExtensionsV1beta1RunAsUserStrategyOptions
    runtime_class: typing.Optional[kubernetes.client.ExtensionsV1beta1RuntimeClassStrategyOptions]
    se_linux: kubernetes.client.ExtensionsV1beta1SELinuxStrategyOptions
    supplemental_groups: kubernetes.client.ExtensionsV1beta1SupplementalGroupsStrategyOptions
    volumes: typing.Optional[list[str]]
    
    def __init__(self, *, allow_privilege_escalation: typing.Optional[bool] = ..., allowed_csi_drivers: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedCSIDriver]] = ..., allowed_capabilities: typing.Optional[list[str]] = ..., allowed_flex_volumes: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedFlexVolume]] = ..., allowed_host_paths: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedHostPath]] = ..., allowed_proc_mount_types: typing.Optional[list[str]] = ..., allowed_unsafe_sysctls: typing.Optional[list[str]] = ..., default_add_capabilities: typing.Optional[list[str]] = ..., default_allow_privilege_escalation: typing.Optional[bool] = ..., forbidden_sysctls: typing.Optional[list[str]] = ..., fs_group: kubernetes.client.ExtensionsV1beta1FSGroupStrategyOptions, host_ipc: typing.Optional[bool] = ..., host_network: typing.Optional[bool] = ..., host_pid: typing.Optional[bool] = ..., host_ports: typing.Optional[list[kubernetes.client.ExtensionsV1beta1HostPortRange]] = ..., privileged: typing.Optional[bool] = ..., read_only_root_filesystem: typing.Optional[bool] = ..., required_drop_capabilities: typing.Optional[list[str]] = ..., run_as_group: typing.Optional[kubernetes.client.ExtensionsV1beta1RunAsGroupStrategyOptions] = ..., run_as_user: kubernetes.client.ExtensionsV1beta1RunAsUserStrategyOptions, runtime_class: typing.Optional[kubernetes.client.ExtensionsV1beta1RuntimeClassStrategyOptions] = ..., se_linux: kubernetes.client.ExtensionsV1beta1SELinuxStrategyOptions, supplemental_groups: kubernetes.client.ExtensionsV1beta1SupplementalGroupsStrategyOptions, volumes: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1PodSecurityPolicySpecDict:
        ...
class ExtensionsV1beta1PodSecurityPolicySpecDict(typing.TypedDict, total=False):
    allowPrivilegeEscalation: typing.Optional[bool]
    allowedCSIDrivers: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedCSIDriverDict]]
    allowedCapabilities: typing.Optional[list[str]]
    allowedFlexVolumes: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedFlexVolumeDict]]
    allowedHostPaths: typing.Optional[list[kubernetes.client.ExtensionsV1beta1AllowedHostPathDict]]
    allowedProcMountTypes: typing.Optional[list[str]]
    allowedUnsafeSysctls: typing.Optional[list[str]]
    defaultAddCapabilities: typing.Optional[list[str]]
    defaultAllowPrivilegeEscalation: typing.Optional[bool]
    forbiddenSysctls: typing.Optional[list[str]]
    fsGroup: kubernetes.client.ExtensionsV1beta1FSGroupStrategyOptionsDict
    hostIPC: typing.Optional[bool]
    hostNetwork: typing.Optional[bool]
    hostPID: typing.Optional[bool]
    hostPorts: typing.Optional[list[kubernetes.client.ExtensionsV1beta1HostPortRangeDict]]
    privileged: typing.Optional[bool]
    readOnlyRootFilesystem: typing.Optional[bool]
    requiredDropCapabilities: typing.Optional[list[str]]
    runAsGroup: typing.Optional[kubernetes.client.ExtensionsV1beta1RunAsGroupStrategyOptionsDict]
    runAsUser: kubernetes.client.ExtensionsV1beta1RunAsUserStrategyOptionsDict
    runtimeClass: typing.Optional[kubernetes.client.ExtensionsV1beta1RuntimeClassStrategyOptionsDict]
    seLinux: kubernetes.client.ExtensionsV1beta1SELinuxStrategyOptionsDict
    supplementalGroups: kubernetes.client.ExtensionsV1beta1SupplementalGroupsStrategyOptionsDict
    volumes: typing.Optional[list[str]]
