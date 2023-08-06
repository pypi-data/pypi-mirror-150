"""
Type annotations for opsworks service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/type_defs/)

Usage::

    ```python
    from mypy_boto3_opsworks.type_defs import AgentVersionTypeDef

    data: AgentVersionTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AppAttributesKeysType,
    AppTypeType,
    ArchitectureType,
    AutoScalingTypeType,
    CloudWatchLogsEncodingType,
    CloudWatchLogsInitialPositionType,
    CloudWatchLogsTimeZoneType,
    DeploymentCommandNameType,
    LayerAttributesKeysType,
    LayerTypeType,
    RootDeviceTypeType,
    SourceTypeType,
    VirtualizationTypeType,
    VolumeTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AgentVersionTypeDef",
    "AppTypeDef",
    "AssignInstanceRequestRequestTypeDef",
    "AssignVolumeRequestRequestTypeDef",
    "AssociateElasticIpRequestRequestTypeDef",
    "AttachElasticLoadBalancerRequestRequestTypeDef",
    "AutoScalingThresholdsTypeDef",
    "BlockDeviceMappingTypeDef",
    "ChefConfigurationResponseMetadataTypeDef",
    "ChefConfigurationTypeDef",
    "CloneStackRequestRequestTypeDef",
    "CloneStackResultTypeDef",
    "CloudWatchLogsConfigurationResponseMetadataTypeDef",
    "CloudWatchLogsConfigurationTypeDef",
    "CloudWatchLogsLogStreamTypeDef",
    "CommandTypeDef",
    "CreateAppRequestRequestTypeDef",
    "CreateAppResultTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "CreateDeploymentResultTypeDef",
    "CreateInstanceRequestRequestTypeDef",
    "CreateInstanceResultTypeDef",
    "CreateLayerRequestRequestTypeDef",
    "CreateLayerRequestStackCreateLayerTypeDef",
    "CreateLayerResultTypeDef",
    "CreateStackRequestRequestTypeDef",
    "CreateStackRequestServiceResourceCreateStackTypeDef",
    "CreateStackResultTypeDef",
    "CreateUserProfileRequestRequestTypeDef",
    "CreateUserProfileResultTypeDef",
    "DataSourceTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteInstanceRequestRequestTypeDef",
    "DeleteLayerRequestRequestTypeDef",
    "DeleteStackRequestRequestTypeDef",
    "DeleteUserProfileRequestRequestTypeDef",
    "DeploymentCommandTypeDef",
    "DeploymentTypeDef",
    "DeregisterEcsClusterRequestRequestTypeDef",
    "DeregisterElasticIpRequestRequestTypeDef",
    "DeregisterInstanceRequestRequestTypeDef",
    "DeregisterRdsDbInstanceRequestRequestTypeDef",
    "DeregisterVolumeRequestRequestTypeDef",
    "DescribeAgentVersionsRequestRequestTypeDef",
    "DescribeAgentVersionsResultTypeDef",
    "DescribeAppsRequestAppExistsWaitTypeDef",
    "DescribeAppsRequestRequestTypeDef",
    "DescribeAppsResultTypeDef",
    "DescribeCommandsRequestRequestTypeDef",
    "DescribeCommandsResultTypeDef",
    "DescribeDeploymentsRequestDeploymentSuccessfulWaitTypeDef",
    "DescribeDeploymentsRequestRequestTypeDef",
    "DescribeDeploymentsResultTypeDef",
    "DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef",
    "DescribeEcsClustersRequestRequestTypeDef",
    "DescribeEcsClustersResultTypeDef",
    "DescribeElasticIpsRequestRequestTypeDef",
    "DescribeElasticIpsResultTypeDef",
    "DescribeElasticLoadBalancersRequestRequestTypeDef",
    "DescribeElasticLoadBalancersResultTypeDef",
    "DescribeInstancesRequestInstanceOnlineWaitTypeDef",
    "DescribeInstancesRequestInstanceRegisteredWaitTypeDef",
    "DescribeInstancesRequestInstanceStoppedWaitTypeDef",
    "DescribeInstancesRequestInstanceTerminatedWaitTypeDef",
    "DescribeInstancesRequestRequestTypeDef",
    "DescribeInstancesResultTypeDef",
    "DescribeLayersRequestRequestTypeDef",
    "DescribeLayersResultTypeDef",
    "DescribeLoadBasedAutoScalingRequestRequestTypeDef",
    "DescribeLoadBasedAutoScalingResultTypeDef",
    "DescribeMyUserProfileResultTypeDef",
    "DescribeOperatingSystemsResponseTypeDef",
    "DescribePermissionsRequestRequestTypeDef",
    "DescribePermissionsResultTypeDef",
    "DescribeRaidArraysRequestRequestTypeDef",
    "DescribeRaidArraysResultTypeDef",
    "DescribeRdsDbInstancesRequestRequestTypeDef",
    "DescribeRdsDbInstancesResultTypeDef",
    "DescribeServiceErrorsRequestRequestTypeDef",
    "DescribeServiceErrorsResultTypeDef",
    "DescribeStackProvisioningParametersRequestRequestTypeDef",
    "DescribeStackProvisioningParametersResultTypeDef",
    "DescribeStackSummaryRequestRequestTypeDef",
    "DescribeStackSummaryResultTypeDef",
    "DescribeStacksRequestRequestTypeDef",
    "DescribeStacksResultTypeDef",
    "DescribeTimeBasedAutoScalingRequestRequestTypeDef",
    "DescribeTimeBasedAutoScalingResultTypeDef",
    "DescribeUserProfilesRequestRequestTypeDef",
    "DescribeUserProfilesResultTypeDef",
    "DescribeVolumesRequestRequestTypeDef",
    "DescribeVolumesResultTypeDef",
    "DetachElasticLoadBalancerRequestRequestTypeDef",
    "DisassociateElasticIpRequestRequestTypeDef",
    "EbsBlockDeviceTypeDef",
    "EcsClusterTypeDef",
    "ElasticIpTypeDef",
    "ElasticLoadBalancerTypeDef",
    "EnvironmentVariableTypeDef",
    "GetHostnameSuggestionRequestRequestTypeDef",
    "GetHostnameSuggestionResultTypeDef",
    "GrantAccessRequestRequestTypeDef",
    "GrantAccessResultTypeDef",
    "InstanceIdentityTypeDef",
    "InstanceTypeDef",
    "InstancesCountResponseMetadataTypeDef",
    "InstancesCountTypeDef",
    "LayerTypeDef",
    "LifecycleEventConfigurationResponseMetadataTypeDef",
    "LifecycleEventConfigurationTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListTagsResultTypeDef",
    "LoadBasedAutoScalingConfigurationTypeDef",
    "OperatingSystemConfigurationManagerTypeDef",
    "OperatingSystemTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionTypeDef",
    "RaidArrayTypeDef",
    "RdsDbInstanceTypeDef",
    "RebootInstanceRequestRequestTypeDef",
    "RecipesResponseMetadataTypeDef",
    "RecipesTypeDef",
    "RegisterEcsClusterRequestRequestTypeDef",
    "RegisterEcsClusterResultTypeDef",
    "RegisterElasticIpRequestRequestTypeDef",
    "RegisterElasticIpResultTypeDef",
    "RegisterInstanceRequestRequestTypeDef",
    "RegisterInstanceResultTypeDef",
    "RegisterRdsDbInstanceRequestRequestTypeDef",
    "RegisterVolumeRequestRequestTypeDef",
    "RegisterVolumeResultTypeDef",
    "ReportedOsTypeDef",
    "ResponseMetadataTypeDef",
    "SelfUserProfileTypeDef",
    "ServiceErrorTypeDef",
    "ServiceResourceLayerRequestTypeDef",
    "ServiceResourceStackRequestTypeDef",
    "ServiceResourceStackSummaryRequestTypeDef",
    "SetLoadBasedAutoScalingRequestRequestTypeDef",
    "SetPermissionRequestRequestTypeDef",
    "SetTimeBasedAutoScalingRequestRequestTypeDef",
    "ShutdownEventConfigurationTypeDef",
    "SourceResponseMetadataTypeDef",
    "SourceTypeDef",
    "SslConfigurationTypeDef",
    "StackConfigurationManagerResponseMetadataTypeDef",
    "StackConfigurationManagerTypeDef",
    "StackSummaryTypeDef",
    "StackTypeDef",
    "StartInstanceRequestRequestTypeDef",
    "StartStackRequestRequestTypeDef",
    "StopInstanceRequestRequestTypeDef",
    "StopStackRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TemporaryCredentialTypeDef",
    "TimeBasedAutoScalingConfigurationTypeDef",
    "UnassignInstanceRequestRequestTypeDef",
    "UnassignVolumeRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppRequestRequestTypeDef",
    "UpdateElasticIpRequestRequestTypeDef",
    "UpdateInstanceRequestRequestTypeDef",
    "UpdateLayerRequestRequestTypeDef",
    "UpdateMyUserProfileRequestRequestTypeDef",
    "UpdateRdsDbInstanceRequestRequestTypeDef",
    "UpdateStackRequestRequestTypeDef",
    "UpdateUserProfileRequestRequestTypeDef",
    "UpdateVolumeRequestRequestTypeDef",
    "UserProfileTypeDef",
    "VolumeConfigurationTypeDef",
    "VolumeTypeDef",
    "WaiterConfigTypeDef",
    "WeeklyAutoScalingScheduleTypeDef",
)

AgentVersionTypeDef = TypedDict(
    "AgentVersionTypeDef",
    {
        "Version": str,
        "ConfigurationManager": "StackConfigurationManagerTypeDef",
    },
    total=False,
)

AppTypeDef = TypedDict(
    "AppTypeDef",
    {
        "AppId": str,
        "StackId": str,
        "Shortname": str,
        "Name": str,
        "Description": str,
        "DataSources": List["DataSourceTypeDef"],
        "Type": AppTypeType,
        "AppSource": "SourceTypeDef",
        "Domains": List[str],
        "EnableSsl": bool,
        "SslConfiguration": "SslConfigurationTypeDef",
        "Attributes": Dict[AppAttributesKeysType, str],
        "CreatedAt": str,
        "Environment": List["EnvironmentVariableTypeDef"],
    },
    total=False,
)

AssignInstanceRequestRequestTypeDef = TypedDict(
    "AssignInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
        "LayerIds": Sequence[str],
    },
)

_RequiredAssignVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredAssignVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)
_OptionalAssignVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalAssignVolumeRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)


class AssignVolumeRequestRequestTypeDef(
    _RequiredAssignVolumeRequestRequestTypeDef, _OptionalAssignVolumeRequestRequestTypeDef
):
    pass


_RequiredAssociateElasticIpRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)
_OptionalAssociateElasticIpRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateElasticIpRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)


class AssociateElasticIpRequestRequestTypeDef(
    _RequiredAssociateElasticIpRequestRequestTypeDef,
    _OptionalAssociateElasticIpRequestRequestTypeDef,
):
    pass


AttachElasticLoadBalancerRequestRequestTypeDef = TypedDict(
    "AttachElasticLoadBalancerRequestRequestTypeDef",
    {
        "ElasticLoadBalancerName": str,
        "LayerId": str,
    },
)

AutoScalingThresholdsTypeDef = TypedDict(
    "AutoScalingThresholdsTypeDef",
    {
        "InstanceCount": int,
        "ThresholdsWaitTime": int,
        "IgnoreMetricsTime": int,
        "CpuThreshold": float,
        "MemoryThreshold": float,
        "LoadThreshold": float,
        "Alarms": List[str],
    },
    total=False,
)

BlockDeviceMappingTypeDef = TypedDict(
    "BlockDeviceMappingTypeDef",
    {
        "DeviceName": str,
        "NoDevice": str,
        "VirtualName": str,
        "Ebs": "EbsBlockDeviceTypeDef",
    },
    total=False,
)

ChefConfigurationResponseMetadataTypeDef = TypedDict(
    "ChefConfigurationResponseMetadataTypeDef",
    {
        "ManageBerkshelf": bool,
        "BerkshelfVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ChefConfigurationTypeDef = TypedDict(
    "ChefConfigurationTypeDef",
    {
        "ManageBerkshelf": bool,
        "BerkshelfVersion": str,
    },
    total=False,
)

_RequiredCloneStackRequestRequestTypeDef = TypedDict(
    "_RequiredCloneStackRequestRequestTypeDef",
    {
        "SourceStackId": str,
        "ServiceRoleArn": str,
    },
)
_OptionalCloneStackRequestRequestTypeDef = TypedDict(
    "_OptionalCloneStackRequestRequestTypeDef",
    {
        "Name": str,
        "Region": str,
        "VpcId": str,
        "Attributes": Mapping[Literal["Color"], str],
        "DefaultInstanceProfileArn": str,
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": "StackConfigurationManagerTypeDef",
        "ChefConfiguration": "ChefConfigurationTypeDef",
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": "SourceTypeDef",
        "DefaultSshKeyName": str,
        "ClonePermissions": bool,
        "CloneAppIds": Sequence[str],
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)


class CloneStackRequestRequestTypeDef(
    _RequiredCloneStackRequestRequestTypeDef, _OptionalCloneStackRequestRequestTypeDef
):
    pass


CloneStackResultTypeDef = TypedDict(
    "CloneStackResultTypeDef",
    {
        "StackId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CloudWatchLogsConfigurationResponseMetadataTypeDef = TypedDict(
    "CloudWatchLogsConfigurationResponseMetadataTypeDef",
    {
        "Enabled": bool,
        "LogStreams": List["CloudWatchLogsLogStreamTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CloudWatchLogsConfigurationTypeDef = TypedDict(
    "CloudWatchLogsConfigurationTypeDef",
    {
        "Enabled": bool,
        "LogStreams": Sequence["CloudWatchLogsLogStreamTypeDef"],
    },
    total=False,
)

CloudWatchLogsLogStreamTypeDef = TypedDict(
    "CloudWatchLogsLogStreamTypeDef",
    {
        "LogGroupName": str,
        "DatetimeFormat": str,
        "TimeZone": CloudWatchLogsTimeZoneType,
        "File": str,
        "FileFingerprintLines": str,
        "MultiLineStartPattern": str,
        "InitialPosition": CloudWatchLogsInitialPositionType,
        "Encoding": CloudWatchLogsEncodingType,
        "BufferDuration": int,
        "BatchCount": int,
        "BatchSize": int,
    },
    total=False,
)

CommandTypeDef = TypedDict(
    "CommandTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "DeploymentId": str,
        "CreatedAt": str,
        "AcknowledgedAt": str,
        "CompletedAt": str,
        "Status": str,
        "ExitCode": int,
        "LogUrl": str,
        "Type": str,
    },
    total=False,
)

_RequiredCreateAppRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppRequestRequestTypeDef",
    {
        "StackId": str,
        "Name": str,
        "Type": AppTypeType,
    },
)
_OptionalCreateAppRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppRequestRequestTypeDef",
    {
        "Shortname": str,
        "Description": str,
        "DataSources": Sequence["DataSourceTypeDef"],
        "AppSource": "SourceTypeDef",
        "Domains": Sequence[str],
        "EnableSsl": bool,
        "SslConfiguration": "SslConfigurationTypeDef",
        "Attributes": Mapping[AppAttributesKeysType, str],
        "Environment": Sequence["EnvironmentVariableTypeDef"],
    },
    total=False,
)


class CreateAppRequestRequestTypeDef(
    _RequiredCreateAppRequestRequestTypeDef, _OptionalCreateAppRequestRequestTypeDef
):
    pass


CreateAppResultTypeDef = TypedDict(
    "CreateAppResultTypeDef",
    {
        "AppId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentRequestRequestTypeDef",
    {
        "StackId": str,
        "Command": "DeploymentCommandTypeDef",
    },
)
_OptionalCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentRequestRequestTypeDef",
    {
        "AppId": str,
        "InstanceIds": Sequence[str],
        "LayerIds": Sequence[str],
        "Comment": str,
        "CustomJson": str,
    },
    total=False,
)


class CreateDeploymentRequestRequestTypeDef(
    _RequiredCreateDeploymentRequestRequestTypeDef, _OptionalCreateDeploymentRequestRequestTypeDef
):
    pass


CreateDeploymentResultTypeDef = TypedDict(
    "CreateDeploymentResultTypeDef",
    {
        "DeploymentId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInstanceRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerIds": Sequence[str],
        "InstanceType": str,
    },
)
_OptionalCreateInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInstanceRequestRequestTypeDef",
    {
        "AutoScalingType": AutoScalingTypeType,
        "Hostname": str,
        "Os": str,
        "AmiId": str,
        "SshKeyName": str,
        "AvailabilityZone": str,
        "VirtualizationType": str,
        "SubnetId": str,
        "Architecture": ArchitectureType,
        "RootDeviceType": RootDeviceTypeType,
        "BlockDeviceMappings": Sequence["BlockDeviceMappingTypeDef"],
        "InstallUpdatesOnBoot": bool,
        "EbsOptimized": bool,
        "AgentVersion": str,
        "Tenancy": str,
    },
    total=False,
)


class CreateInstanceRequestRequestTypeDef(
    _RequiredCreateInstanceRequestRequestTypeDef, _OptionalCreateInstanceRequestRequestTypeDef
):
    pass


CreateInstanceResultTypeDef = TypedDict(
    "CreateInstanceResultTypeDef",
    {
        "InstanceId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateLayerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLayerRequestRequestTypeDef",
    {
        "StackId": str,
        "Type": LayerTypeType,
        "Name": str,
        "Shortname": str,
    },
)
_OptionalCreateLayerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLayerRequestRequestTypeDef",
    {
        "Attributes": Mapping[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": "CloudWatchLogsConfigurationTypeDef",
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": Sequence[str],
        "Packages": Sequence[str],
        "VolumeConfigurations": Sequence["VolumeConfigurationTypeDef"],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "CustomRecipes": "RecipesTypeDef",
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": "LifecycleEventConfigurationTypeDef",
    },
    total=False,
)


class CreateLayerRequestRequestTypeDef(
    _RequiredCreateLayerRequestRequestTypeDef, _OptionalCreateLayerRequestRequestTypeDef
):
    pass


_RequiredCreateLayerRequestStackCreateLayerTypeDef = TypedDict(
    "_RequiredCreateLayerRequestStackCreateLayerTypeDef",
    {
        "Type": LayerTypeType,
        "Name": str,
        "Shortname": str,
    },
)
_OptionalCreateLayerRequestStackCreateLayerTypeDef = TypedDict(
    "_OptionalCreateLayerRequestStackCreateLayerTypeDef",
    {
        "Attributes": Mapping[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": "CloudWatchLogsConfigurationTypeDef",
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": Sequence[str],
        "Packages": Sequence[str],
        "VolumeConfigurations": Sequence["VolumeConfigurationTypeDef"],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "CustomRecipes": "RecipesTypeDef",
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": "LifecycleEventConfigurationTypeDef",
    },
    total=False,
)


class CreateLayerRequestStackCreateLayerTypeDef(
    _RequiredCreateLayerRequestStackCreateLayerTypeDef,
    _OptionalCreateLayerRequestStackCreateLayerTypeDef,
):
    pass


CreateLayerResultTypeDef = TypedDict(
    "CreateLayerResultTypeDef",
    {
        "LayerId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateStackRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStackRequestRequestTypeDef",
    {
        "Name": str,
        "Region": str,
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
    },
)
_OptionalCreateStackRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStackRequestRequestTypeDef",
    {
        "VpcId": str,
        "Attributes": Mapping[Literal["Color"], str],
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": "StackConfigurationManagerTypeDef",
        "ChefConfiguration": "ChefConfigurationTypeDef",
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": "SourceTypeDef",
        "DefaultSshKeyName": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)


class CreateStackRequestRequestTypeDef(
    _RequiredCreateStackRequestRequestTypeDef, _OptionalCreateStackRequestRequestTypeDef
):
    pass


_RequiredCreateStackRequestServiceResourceCreateStackTypeDef = TypedDict(
    "_RequiredCreateStackRequestServiceResourceCreateStackTypeDef",
    {
        "Name": str,
        "Region": str,
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
    },
)
_OptionalCreateStackRequestServiceResourceCreateStackTypeDef = TypedDict(
    "_OptionalCreateStackRequestServiceResourceCreateStackTypeDef",
    {
        "VpcId": str,
        "Attributes": Mapping[Literal["Color"], str],
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": "StackConfigurationManagerTypeDef",
        "ChefConfiguration": "ChefConfigurationTypeDef",
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": "SourceTypeDef",
        "DefaultSshKeyName": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)


class CreateStackRequestServiceResourceCreateStackTypeDef(
    _RequiredCreateStackRequestServiceResourceCreateStackTypeDef,
    _OptionalCreateStackRequestServiceResourceCreateStackTypeDef,
):
    pass


CreateStackResultTypeDef = TypedDict(
    "CreateStackResultTypeDef",
    {
        "StackId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserProfileRequestRequestTypeDef",
    {
        "IamUserArn": str,
    },
)
_OptionalCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserProfileRequestRequestTypeDef",
    {
        "SshUsername": str,
        "SshPublicKey": str,
        "AllowSelfManagement": bool,
    },
    total=False,
)


class CreateUserProfileRequestRequestTypeDef(
    _RequiredCreateUserProfileRequestRequestTypeDef, _OptionalCreateUserProfileRequestRequestTypeDef
):
    pass


CreateUserProfileResultTypeDef = TypedDict(
    "CreateUserProfileResultTypeDef",
    {
        "IamUserArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Type": str,
        "Arn": str,
        "DatabaseName": str,
    },
    total=False,
)

DeleteAppRequestRequestTypeDef = TypedDict(
    "DeleteAppRequestRequestTypeDef",
    {
        "AppId": str,
    },
)

_RequiredDeleteInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDeleteInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteInstanceRequestRequestTypeDef",
    {
        "DeleteElasticIp": bool,
        "DeleteVolumes": bool,
    },
    total=False,
)


class DeleteInstanceRequestRequestTypeDef(
    _RequiredDeleteInstanceRequestRequestTypeDef, _OptionalDeleteInstanceRequestRequestTypeDef
):
    pass


DeleteLayerRequestRequestTypeDef = TypedDict(
    "DeleteLayerRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)

DeleteStackRequestRequestTypeDef = TypedDict(
    "DeleteStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

DeleteUserProfileRequestRequestTypeDef = TypedDict(
    "DeleteUserProfileRequestRequestTypeDef",
    {
        "IamUserArn": str,
    },
)

_RequiredDeploymentCommandTypeDef = TypedDict(
    "_RequiredDeploymentCommandTypeDef",
    {
        "Name": DeploymentCommandNameType,
    },
)
_OptionalDeploymentCommandTypeDef = TypedDict(
    "_OptionalDeploymentCommandTypeDef",
    {
        "Args": Mapping[str, Sequence[str]],
    },
    total=False,
)


class DeploymentCommandTypeDef(
    _RequiredDeploymentCommandTypeDef, _OptionalDeploymentCommandTypeDef
):
    pass


DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "DeploymentId": str,
        "StackId": str,
        "AppId": str,
        "CreatedAt": str,
        "CompletedAt": str,
        "Duration": int,
        "IamUserArn": str,
        "Comment": str,
        "Command": "DeploymentCommandTypeDef",
        "Status": str,
        "CustomJson": str,
        "InstanceIds": List[str],
    },
    total=False,
)

DeregisterEcsClusterRequestRequestTypeDef = TypedDict(
    "DeregisterEcsClusterRequestRequestTypeDef",
    {
        "EcsClusterArn": str,
    },
)

DeregisterElasticIpRequestRequestTypeDef = TypedDict(
    "DeregisterElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)

DeregisterInstanceRequestRequestTypeDef = TypedDict(
    "DeregisterInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

DeregisterRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "DeregisterRdsDbInstanceRequestRequestTypeDef",
    {
        "RdsDbInstanceArn": str,
    },
)

DeregisterVolumeRequestRequestTypeDef = TypedDict(
    "DeregisterVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)

DescribeAgentVersionsRequestRequestTypeDef = TypedDict(
    "DescribeAgentVersionsRequestRequestTypeDef",
    {
        "StackId": str,
        "ConfigurationManager": "StackConfigurationManagerTypeDef",
    },
    total=False,
)

DescribeAgentVersionsResultTypeDef = TypedDict(
    "DescribeAgentVersionsResultTypeDef",
    {
        "AgentVersions": List["AgentVersionTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeAppsRequestAppExistsWaitTypeDef = TypedDict(
    "DescribeAppsRequestAppExistsWaitTypeDef",
    {
        "StackId": str,
        "AppIds": Sequence[str],
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)

DescribeAppsRequestRequestTypeDef = TypedDict(
    "DescribeAppsRequestRequestTypeDef",
    {
        "StackId": str,
        "AppIds": Sequence[str],
    },
    total=False,
)

DescribeAppsResultTypeDef = TypedDict(
    "DescribeAppsResultTypeDef",
    {
        "Apps": List["AppTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCommandsRequestRequestTypeDef = TypedDict(
    "DescribeCommandsRequestRequestTypeDef",
    {
        "DeploymentId": str,
        "InstanceId": str,
        "CommandIds": Sequence[str],
    },
    total=False,
)

DescribeCommandsResultTypeDef = TypedDict(
    "DescribeCommandsResultTypeDef",
    {
        "Commands": List["CommandTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDeploymentsRequestDeploymentSuccessfulWaitTypeDef = TypedDict(
    "DescribeDeploymentsRequestDeploymentSuccessfulWaitTypeDef",
    {
        "StackId": str,
        "AppId": str,
        "DeploymentIds": Sequence[str],
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)

DescribeDeploymentsRequestRequestTypeDef = TypedDict(
    "DescribeDeploymentsRequestRequestTypeDef",
    {
        "StackId": str,
        "AppId": str,
        "DeploymentIds": Sequence[str],
    },
    total=False,
)

DescribeDeploymentsResultTypeDef = TypedDict(
    "DescribeDeploymentsResultTypeDef",
    {
        "Deployments": List["DeploymentTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef = TypedDict(
    "DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef",
    {
        "EcsClusterArns": Sequence[str],
        "StackId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEcsClustersRequestRequestTypeDef = TypedDict(
    "DescribeEcsClustersRequestRequestTypeDef",
    {
        "EcsClusterArns": Sequence[str],
        "StackId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeEcsClustersResultTypeDef = TypedDict(
    "DescribeEcsClustersResultTypeDef",
    {
        "EcsClusters": List["EcsClusterTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeElasticIpsRequestRequestTypeDef = TypedDict(
    "DescribeElasticIpsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "StackId": str,
        "Ips": Sequence[str],
    },
    total=False,
)

DescribeElasticIpsResultTypeDef = TypedDict(
    "DescribeElasticIpsResultTypeDef",
    {
        "ElasticIps": List["ElasticIpTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeElasticLoadBalancersRequestRequestTypeDef = TypedDict(
    "DescribeElasticLoadBalancersRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerIds": Sequence[str],
    },
    total=False,
)

DescribeElasticLoadBalancersResultTypeDef = TypedDict(
    "DescribeElasticLoadBalancersResultTypeDef",
    {
        "ElasticLoadBalancers": List["ElasticLoadBalancerTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeInstancesRequestInstanceOnlineWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceOnlineWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)

DescribeInstancesRequestInstanceRegisteredWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceRegisteredWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)

DescribeInstancesRequestInstanceStoppedWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceStoppedWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)

DescribeInstancesRequestInstanceTerminatedWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceTerminatedWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)

DescribeInstancesRequestRequestTypeDef = TypedDict(
    "DescribeInstancesRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
    },
    total=False,
)

DescribeInstancesResultTypeDef = TypedDict(
    "DescribeInstancesResultTypeDef",
    {
        "Instances": List["InstanceTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeLayersRequestRequestTypeDef = TypedDict(
    "DescribeLayersRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerIds": Sequence[str],
    },
    total=False,
)

DescribeLayersResultTypeDef = TypedDict(
    "DescribeLayersResultTypeDef",
    {
        "Layers": List["LayerTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeLoadBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "DescribeLoadBasedAutoScalingRequestRequestTypeDef",
    {
        "LayerIds": Sequence[str],
    },
)

DescribeLoadBasedAutoScalingResultTypeDef = TypedDict(
    "DescribeLoadBasedAutoScalingResultTypeDef",
    {
        "LoadBasedAutoScalingConfigurations": List["LoadBasedAutoScalingConfigurationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeMyUserProfileResultTypeDef = TypedDict(
    "DescribeMyUserProfileResultTypeDef",
    {
        "UserProfile": "SelfUserProfileTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOperatingSystemsResponseTypeDef = TypedDict(
    "DescribeOperatingSystemsResponseTypeDef",
    {
        "OperatingSystems": List["OperatingSystemTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePermissionsRequestRequestTypeDef = TypedDict(
    "DescribePermissionsRequestRequestTypeDef",
    {
        "IamUserArn": str,
        "StackId": str,
    },
    total=False,
)

DescribePermissionsResultTypeDef = TypedDict(
    "DescribePermissionsResultTypeDef",
    {
        "Permissions": List["PermissionTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRaidArraysRequestRequestTypeDef = TypedDict(
    "DescribeRaidArraysRequestRequestTypeDef",
    {
        "InstanceId": str,
        "StackId": str,
        "RaidArrayIds": Sequence[str],
    },
    total=False,
)

DescribeRaidArraysResultTypeDef = TypedDict(
    "DescribeRaidArraysResultTypeDef",
    {
        "RaidArrays": List["RaidArrayTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeRdsDbInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRdsDbInstancesRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalDescribeRdsDbInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRdsDbInstancesRequestRequestTypeDef",
    {
        "RdsDbInstanceArns": Sequence[str],
    },
    total=False,
)


class DescribeRdsDbInstancesRequestRequestTypeDef(
    _RequiredDescribeRdsDbInstancesRequestRequestTypeDef,
    _OptionalDescribeRdsDbInstancesRequestRequestTypeDef,
):
    pass


DescribeRdsDbInstancesResultTypeDef = TypedDict(
    "DescribeRdsDbInstancesResultTypeDef",
    {
        "RdsDbInstances": List["RdsDbInstanceTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeServiceErrorsRequestRequestTypeDef = TypedDict(
    "DescribeServiceErrorsRequestRequestTypeDef",
    {
        "StackId": str,
        "InstanceId": str,
        "ServiceErrorIds": Sequence[str],
    },
    total=False,
)

DescribeServiceErrorsResultTypeDef = TypedDict(
    "DescribeServiceErrorsResultTypeDef",
    {
        "ServiceErrors": List["ServiceErrorTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeStackProvisioningParametersRequestRequestTypeDef = TypedDict(
    "DescribeStackProvisioningParametersRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

DescribeStackProvisioningParametersResultTypeDef = TypedDict(
    "DescribeStackProvisioningParametersResultTypeDef",
    {
        "AgentInstallerUrl": str,
        "Parameters": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeStackSummaryRequestRequestTypeDef = TypedDict(
    "DescribeStackSummaryRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

DescribeStackSummaryResultTypeDef = TypedDict(
    "DescribeStackSummaryResultTypeDef",
    {
        "StackSummary": "StackSummaryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeStacksRequestRequestTypeDef = TypedDict(
    "DescribeStacksRequestRequestTypeDef",
    {
        "StackIds": Sequence[str],
    },
    total=False,
)

DescribeStacksResultTypeDef = TypedDict(
    "DescribeStacksResultTypeDef",
    {
        "Stacks": List["StackTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTimeBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "DescribeTimeBasedAutoScalingRequestRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
)

DescribeTimeBasedAutoScalingResultTypeDef = TypedDict(
    "DescribeTimeBasedAutoScalingResultTypeDef",
    {
        "TimeBasedAutoScalingConfigurations": List["TimeBasedAutoScalingConfigurationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeUserProfilesRequestRequestTypeDef = TypedDict(
    "DescribeUserProfilesRequestRequestTypeDef",
    {
        "IamUserArns": Sequence[str],
    },
    total=False,
)

DescribeUserProfilesResultTypeDef = TypedDict(
    "DescribeUserProfilesResultTypeDef",
    {
        "UserProfiles": List["UserProfileTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeVolumesRequestRequestTypeDef = TypedDict(
    "DescribeVolumesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "StackId": str,
        "RaidArrayId": str,
        "VolumeIds": Sequence[str],
    },
    total=False,
)

DescribeVolumesResultTypeDef = TypedDict(
    "DescribeVolumesResultTypeDef",
    {
        "Volumes": List["VolumeTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DetachElasticLoadBalancerRequestRequestTypeDef = TypedDict(
    "DetachElasticLoadBalancerRequestRequestTypeDef",
    {
        "ElasticLoadBalancerName": str,
        "LayerId": str,
    },
)

DisassociateElasticIpRequestRequestTypeDef = TypedDict(
    "DisassociateElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)

EbsBlockDeviceTypeDef = TypedDict(
    "EbsBlockDeviceTypeDef",
    {
        "SnapshotId": str,
        "Iops": int,
        "VolumeSize": int,
        "VolumeType": VolumeTypeType,
        "DeleteOnTermination": bool,
    },
    total=False,
)

EcsClusterTypeDef = TypedDict(
    "EcsClusterTypeDef",
    {
        "EcsClusterArn": str,
        "EcsClusterName": str,
        "StackId": str,
        "RegisteredAt": str,
    },
    total=False,
)

ElasticIpTypeDef = TypedDict(
    "ElasticIpTypeDef",
    {
        "Ip": str,
        "Name": str,
        "Domain": str,
        "Region": str,
        "InstanceId": str,
    },
    total=False,
)

ElasticLoadBalancerTypeDef = TypedDict(
    "ElasticLoadBalancerTypeDef",
    {
        "ElasticLoadBalancerName": str,
        "Region": str,
        "DnsName": str,
        "StackId": str,
        "LayerId": str,
        "VpcId": str,
        "AvailabilityZones": List[str],
        "SubnetIds": List[str],
        "Ec2InstanceIds": List[str],
    },
    total=False,
)

_RequiredEnvironmentVariableTypeDef = TypedDict(
    "_RequiredEnvironmentVariableTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)
_OptionalEnvironmentVariableTypeDef = TypedDict(
    "_OptionalEnvironmentVariableTypeDef",
    {
        "Secure": bool,
    },
    total=False,
)


class EnvironmentVariableTypeDef(
    _RequiredEnvironmentVariableTypeDef, _OptionalEnvironmentVariableTypeDef
):
    pass


GetHostnameSuggestionRequestRequestTypeDef = TypedDict(
    "GetHostnameSuggestionRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)

GetHostnameSuggestionResultTypeDef = TypedDict(
    "GetHostnameSuggestionResultTypeDef",
    {
        "LayerId": str,
        "Hostname": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGrantAccessRequestRequestTypeDef = TypedDict(
    "_RequiredGrantAccessRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalGrantAccessRequestRequestTypeDef = TypedDict(
    "_OptionalGrantAccessRequestRequestTypeDef",
    {
        "ValidForInMinutes": int,
    },
    total=False,
)


class GrantAccessRequestRequestTypeDef(
    _RequiredGrantAccessRequestRequestTypeDef, _OptionalGrantAccessRequestRequestTypeDef
):
    pass


GrantAccessResultTypeDef = TypedDict(
    "GrantAccessResultTypeDef",
    {
        "TemporaryCredential": "TemporaryCredentialTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InstanceIdentityTypeDef = TypedDict(
    "InstanceIdentityTypeDef",
    {
        "Document": str,
        "Signature": str,
    },
    total=False,
)

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "AgentVersion": str,
        "AmiId": str,
        "Architecture": ArchitectureType,
        "Arn": str,
        "AutoScalingType": AutoScalingTypeType,
        "AvailabilityZone": str,
        "BlockDeviceMappings": List["BlockDeviceMappingTypeDef"],
        "CreatedAt": str,
        "EbsOptimized": bool,
        "Ec2InstanceId": str,
        "EcsClusterArn": str,
        "EcsContainerInstanceArn": str,
        "ElasticIp": str,
        "Hostname": str,
        "InfrastructureClass": str,
        "InstallUpdatesOnBoot": bool,
        "InstanceId": str,
        "InstanceProfileArn": str,
        "InstanceType": str,
        "LastServiceErrorId": str,
        "LayerIds": List[str],
        "Os": str,
        "Platform": str,
        "PrivateDns": str,
        "PrivateIp": str,
        "PublicDns": str,
        "PublicIp": str,
        "RegisteredBy": str,
        "ReportedAgentVersion": str,
        "ReportedOs": "ReportedOsTypeDef",
        "RootDeviceType": RootDeviceTypeType,
        "RootDeviceVolumeId": str,
        "SecurityGroupIds": List[str],
        "SshHostDsaKeyFingerprint": str,
        "SshHostRsaKeyFingerprint": str,
        "SshKeyName": str,
        "StackId": str,
        "Status": str,
        "SubnetId": str,
        "Tenancy": str,
        "VirtualizationType": VirtualizationTypeType,
    },
    total=False,
)

InstancesCountResponseMetadataTypeDef = TypedDict(
    "InstancesCountResponseMetadataTypeDef",
    {
        "Assigning": int,
        "Booting": int,
        "ConnectionLost": int,
        "Deregistering": int,
        "Online": int,
        "Pending": int,
        "Rebooting": int,
        "Registered": int,
        "Registering": int,
        "Requested": int,
        "RunningSetup": int,
        "SetupFailed": int,
        "ShuttingDown": int,
        "StartFailed": int,
        "StopFailed": int,
        "Stopped": int,
        "Stopping": int,
        "Terminated": int,
        "Terminating": int,
        "Unassigning": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InstancesCountTypeDef = TypedDict(
    "InstancesCountTypeDef",
    {
        "Assigning": int,
        "Booting": int,
        "ConnectionLost": int,
        "Deregistering": int,
        "Online": int,
        "Pending": int,
        "Rebooting": int,
        "Registered": int,
        "Registering": int,
        "Requested": int,
        "RunningSetup": int,
        "SetupFailed": int,
        "ShuttingDown": int,
        "StartFailed": int,
        "StopFailed": int,
        "Stopped": int,
        "Stopping": int,
        "Terminated": int,
        "Terminating": int,
        "Unassigning": int,
    },
    total=False,
)

LayerTypeDef = TypedDict(
    "LayerTypeDef",
    {
        "Arn": str,
        "StackId": str,
        "LayerId": str,
        "Type": LayerTypeType,
        "Name": str,
        "Shortname": str,
        "Attributes": Dict[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": "CloudWatchLogsConfigurationTypeDef",
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": List[str],
        "DefaultSecurityGroupNames": List[str],
        "Packages": List[str],
        "VolumeConfigurations": List["VolumeConfigurationTypeDef"],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "DefaultRecipes": "RecipesTypeDef",
        "CustomRecipes": "RecipesTypeDef",
        "CreatedAt": str,
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": "LifecycleEventConfigurationTypeDef",
    },
    total=False,
)

LifecycleEventConfigurationResponseMetadataTypeDef = TypedDict(
    "LifecycleEventConfigurationResponseMetadataTypeDef",
    {
        "Shutdown": "ShutdownEventConfigurationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LifecycleEventConfigurationTypeDef = TypedDict(
    "LifecycleEventConfigurationTypeDef",
    {
        "Shutdown": "ShutdownEventConfigurationTypeDef",
    },
    total=False,
)

_RequiredListTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListTagsRequestRequestTypeDef(
    _RequiredListTagsRequestRequestTypeDef, _OptionalListTagsRequestRequestTypeDef
):
    pass


ListTagsResultTypeDef = TypedDict(
    "ListTagsResultTypeDef",
    {
        "Tags": Dict[str, str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LoadBasedAutoScalingConfigurationTypeDef = TypedDict(
    "LoadBasedAutoScalingConfigurationTypeDef",
    {
        "LayerId": str,
        "Enable": bool,
        "UpScaling": "AutoScalingThresholdsTypeDef",
        "DownScaling": "AutoScalingThresholdsTypeDef",
    },
    total=False,
)

OperatingSystemConfigurationManagerTypeDef = TypedDict(
    "OperatingSystemConfigurationManagerTypeDef",
    {
        "Name": str,
        "Version": str,
    },
    total=False,
)

OperatingSystemTypeDef = TypedDict(
    "OperatingSystemTypeDef",
    {
        "Name": str,
        "Id": str,
        "Type": str,
        "ConfigurationManagers": List["OperatingSystemConfigurationManagerTypeDef"],
        "ReportedName": str,
        "ReportedVersion": str,
        "Supported": bool,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "StackId": str,
        "IamUserArn": str,
        "AllowSsh": bool,
        "AllowSudo": bool,
        "Level": str,
    },
    total=False,
)

RaidArrayTypeDef = TypedDict(
    "RaidArrayTypeDef",
    {
        "RaidArrayId": str,
        "InstanceId": str,
        "Name": str,
        "RaidLevel": int,
        "NumberOfDisks": int,
        "Size": int,
        "Device": str,
        "MountPoint": str,
        "AvailabilityZone": str,
        "CreatedAt": str,
        "StackId": str,
        "VolumeType": str,
        "Iops": int,
    },
    total=False,
)

RdsDbInstanceTypeDef = TypedDict(
    "RdsDbInstanceTypeDef",
    {
        "RdsDbInstanceArn": str,
        "DbInstanceIdentifier": str,
        "DbUser": str,
        "DbPassword": str,
        "Region": str,
        "Address": str,
        "Engine": str,
        "StackId": str,
        "MissingOnRds": bool,
    },
    total=False,
)

RebootInstanceRequestRequestTypeDef = TypedDict(
    "RebootInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

RecipesResponseMetadataTypeDef = TypedDict(
    "RecipesResponseMetadataTypeDef",
    {
        "Setup": List[str],
        "Configure": List[str],
        "Deploy": List[str],
        "Undeploy": List[str],
        "Shutdown": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecipesTypeDef = TypedDict(
    "RecipesTypeDef",
    {
        "Setup": Sequence[str],
        "Configure": Sequence[str],
        "Deploy": Sequence[str],
        "Undeploy": Sequence[str],
        "Shutdown": Sequence[str],
    },
    total=False,
)

RegisterEcsClusterRequestRequestTypeDef = TypedDict(
    "RegisterEcsClusterRequestRequestTypeDef",
    {
        "EcsClusterArn": str,
        "StackId": str,
    },
)

RegisterEcsClusterResultTypeDef = TypedDict(
    "RegisterEcsClusterResultTypeDef",
    {
        "EcsClusterArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RegisterElasticIpRequestRequestTypeDef = TypedDict(
    "RegisterElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
        "StackId": str,
    },
)

RegisterElasticIpResultTypeDef = TypedDict(
    "RegisterElasticIpResultTypeDef",
    {
        "ElasticIp": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredRegisterInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterInstanceRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalRegisterInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterInstanceRequestRequestTypeDef",
    {
        "Hostname": str,
        "PublicIp": str,
        "PrivateIp": str,
        "RsaPublicKey": str,
        "RsaPublicKeyFingerprint": str,
        "InstanceIdentity": "InstanceIdentityTypeDef",
    },
    total=False,
)


class RegisterInstanceRequestRequestTypeDef(
    _RequiredRegisterInstanceRequestRequestTypeDef, _OptionalRegisterInstanceRequestRequestTypeDef
):
    pass


RegisterInstanceResultTypeDef = TypedDict(
    "RegisterInstanceResultTypeDef",
    {
        "InstanceId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RegisterRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "RegisterRdsDbInstanceRequestRequestTypeDef",
    {
        "StackId": str,
        "RdsDbInstanceArn": str,
        "DbUser": str,
        "DbPassword": str,
    },
)

_RequiredRegisterVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterVolumeRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalRegisterVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterVolumeRequestRequestTypeDef",
    {
        "Ec2VolumeId": str,
    },
    total=False,
)


class RegisterVolumeRequestRequestTypeDef(
    _RequiredRegisterVolumeRequestRequestTypeDef, _OptionalRegisterVolumeRequestRequestTypeDef
):
    pass


RegisterVolumeResultTypeDef = TypedDict(
    "RegisterVolumeResultTypeDef",
    {
        "VolumeId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReportedOsTypeDef = TypedDict(
    "ReportedOsTypeDef",
    {
        "Family": str,
        "Name": str,
        "Version": str,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

SelfUserProfileTypeDef = TypedDict(
    "SelfUserProfileTypeDef",
    {
        "IamUserArn": str,
        "Name": str,
        "SshUsername": str,
        "SshPublicKey": str,
    },
    total=False,
)

ServiceErrorTypeDef = TypedDict(
    "ServiceErrorTypeDef",
    {
        "ServiceErrorId": str,
        "StackId": str,
        "InstanceId": str,
        "Type": str,
        "Message": str,
        "CreatedAt": str,
    },
    total=False,
)

ServiceResourceLayerRequestTypeDef = TypedDict(
    "ServiceResourceLayerRequestTypeDef",
    {
        "id": str,
    },
)

ServiceResourceStackRequestTypeDef = TypedDict(
    "ServiceResourceStackRequestTypeDef",
    {
        "id": str,
    },
)

ServiceResourceStackSummaryRequestTypeDef = TypedDict(
    "ServiceResourceStackSummaryRequestTypeDef",
    {
        "stack_id": str,
    },
)

_RequiredSetLoadBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_RequiredSetLoadBasedAutoScalingRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)
_OptionalSetLoadBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_OptionalSetLoadBasedAutoScalingRequestRequestTypeDef",
    {
        "Enable": bool,
        "UpScaling": "AutoScalingThresholdsTypeDef",
        "DownScaling": "AutoScalingThresholdsTypeDef",
    },
    total=False,
)


class SetLoadBasedAutoScalingRequestRequestTypeDef(
    _RequiredSetLoadBasedAutoScalingRequestRequestTypeDef,
    _OptionalSetLoadBasedAutoScalingRequestRequestTypeDef,
):
    pass


_RequiredSetPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredSetPermissionRequestRequestTypeDef",
    {
        "StackId": str,
        "IamUserArn": str,
    },
)
_OptionalSetPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalSetPermissionRequestRequestTypeDef",
    {
        "AllowSsh": bool,
        "AllowSudo": bool,
        "Level": str,
    },
    total=False,
)


class SetPermissionRequestRequestTypeDef(
    _RequiredSetPermissionRequestRequestTypeDef, _OptionalSetPermissionRequestRequestTypeDef
):
    pass


_RequiredSetTimeBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_RequiredSetTimeBasedAutoScalingRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSetTimeBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_OptionalSetTimeBasedAutoScalingRequestRequestTypeDef",
    {
        "AutoScalingSchedule": "WeeklyAutoScalingScheduleTypeDef",
    },
    total=False,
)


class SetTimeBasedAutoScalingRequestRequestTypeDef(
    _RequiredSetTimeBasedAutoScalingRequestRequestTypeDef,
    _OptionalSetTimeBasedAutoScalingRequestRequestTypeDef,
):
    pass


ShutdownEventConfigurationTypeDef = TypedDict(
    "ShutdownEventConfigurationTypeDef",
    {
        "ExecutionTimeout": int,
        "DelayUntilElbConnectionsDrained": bool,
    },
    total=False,
)

SourceResponseMetadataTypeDef = TypedDict(
    "SourceResponseMetadataTypeDef",
    {
        "Type": SourceTypeType,
        "Url": str,
        "Username": str,
        "Password": str,
        "SshKey": str,
        "Revision": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SourceTypeDef = TypedDict(
    "SourceTypeDef",
    {
        "Type": SourceTypeType,
        "Url": str,
        "Username": str,
        "Password": str,
        "SshKey": str,
        "Revision": str,
    },
    total=False,
)

_RequiredSslConfigurationTypeDef = TypedDict(
    "_RequiredSslConfigurationTypeDef",
    {
        "Certificate": str,
        "PrivateKey": str,
    },
)
_OptionalSslConfigurationTypeDef = TypedDict(
    "_OptionalSslConfigurationTypeDef",
    {
        "Chain": str,
    },
    total=False,
)


class SslConfigurationTypeDef(_RequiredSslConfigurationTypeDef, _OptionalSslConfigurationTypeDef):
    pass


StackConfigurationManagerResponseMetadataTypeDef = TypedDict(
    "StackConfigurationManagerResponseMetadataTypeDef",
    {
        "Name": str,
        "Version": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StackConfigurationManagerTypeDef = TypedDict(
    "StackConfigurationManagerTypeDef",
    {
        "Name": str,
        "Version": str,
    },
    total=False,
)

StackSummaryTypeDef = TypedDict(
    "StackSummaryTypeDef",
    {
        "StackId": str,
        "Name": str,
        "Arn": str,
        "LayersCount": int,
        "AppsCount": int,
        "InstancesCount": "InstancesCountTypeDef",
    },
    total=False,
)

StackTypeDef = TypedDict(
    "StackTypeDef",
    {
        "StackId": str,
        "Name": str,
        "Arn": str,
        "Region": str,
        "VpcId": str,
        "Attributes": Dict[Literal["Color"], str],
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": "StackConfigurationManagerTypeDef",
        "ChefConfiguration": "ChefConfigurationTypeDef",
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": "SourceTypeDef",
        "DefaultSshKeyName": str,
        "CreatedAt": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)

StartInstanceRequestRequestTypeDef = TypedDict(
    "StartInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

StartStackRequestRequestTypeDef = TypedDict(
    "StartStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

_RequiredStopInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredStopInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalStopInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalStopInstanceRequestRequestTypeDef",
    {
        "Force": bool,
    },
    total=False,
)


class StopInstanceRequestRequestTypeDef(
    _RequiredStopInstanceRequestRequestTypeDef, _OptionalStopInstanceRequestRequestTypeDef
):
    pass


StopStackRequestRequestTypeDef = TypedDict(
    "StopStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

TemporaryCredentialTypeDef = TypedDict(
    "TemporaryCredentialTypeDef",
    {
        "Username": str,
        "Password": str,
        "ValidForInMinutes": int,
        "InstanceId": str,
    },
    total=False,
)

TimeBasedAutoScalingConfigurationTypeDef = TypedDict(
    "TimeBasedAutoScalingConfigurationTypeDef",
    {
        "InstanceId": str,
        "AutoScalingSchedule": "WeeklyAutoScalingScheduleTypeDef",
    },
    total=False,
)

UnassignInstanceRequestRequestTypeDef = TypedDict(
    "UnassignInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

UnassignVolumeRequestRequestTypeDef = TypedDict(
    "UnassignVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAppRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppRequestRequestTypeDef",
    {
        "AppId": str,
    },
)
_OptionalUpdateAppRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "DataSources": Sequence["DataSourceTypeDef"],
        "Type": AppTypeType,
        "AppSource": "SourceTypeDef",
        "Domains": Sequence[str],
        "EnableSsl": bool,
        "SslConfiguration": "SslConfigurationTypeDef",
        "Attributes": Mapping[AppAttributesKeysType, str],
        "Environment": Sequence["EnvironmentVariableTypeDef"],
    },
    total=False,
)


class UpdateAppRequestRequestTypeDef(
    _RequiredUpdateAppRequestRequestTypeDef, _OptionalUpdateAppRequestRequestTypeDef
):
    pass


_RequiredUpdateElasticIpRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)
_OptionalUpdateElasticIpRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateElasticIpRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateElasticIpRequestRequestTypeDef(
    _RequiredUpdateElasticIpRequestRequestTypeDef, _OptionalUpdateElasticIpRequestRequestTypeDef
):
    pass


_RequiredUpdateInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalUpdateInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInstanceRequestRequestTypeDef",
    {
        "LayerIds": Sequence[str],
        "InstanceType": str,
        "AutoScalingType": AutoScalingTypeType,
        "Hostname": str,
        "Os": str,
        "AmiId": str,
        "SshKeyName": str,
        "Architecture": ArchitectureType,
        "InstallUpdatesOnBoot": bool,
        "EbsOptimized": bool,
        "AgentVersion": str,
    },
    total=False,
)


class UpdateInstanceRequestRequestTypeDef(
    _RequiredUpdateInstanceRequestRequestTypeDef, _OptionalUpdateInstanceRequestRequestTypeDef
):
    pass


_RequiredUpdateLayerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLayerRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)
_OptionalUpdateLayerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLayerRequestRequestTypeDef",
    {
        "Name": str,
        "Shortname": str,
        "Attributes": Mapping[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": "CloudWatchLogsConfigurationTypeDef",
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": Sequence[str],
        "Packages": Sequence[str],
        "VolumeConfigurations": Sequence["VolumeConfigurationTypeDef"],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "CustomRecipes": "RecipesTypeDef",
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": "LifecycleEventConfigurationTypeDef",
    },
    total=False,
)


class UpdateLayerRequestRequestTypeDef(
    _RequiredUpdateLayerRequestRequestTypeDef, _OptionalUpdateLayerRequestRequestTypeDef
):
    pass


UpdateMyUserProfileRequestRequestTypeDef = TypedDict(
    "UpdateMyUserProfileRequestRequestTypeDef",
    {
        "SshPublicKey": str,
    },
    total=False,
)

_RequiredUpdateRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRdsDbInstanceRequestRequestTypeDef",
    {
        "RdsDbInstanceArn": str,
    },
)
_OptionalUpdateRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRdsDbInstanceRequestRequestTypeDef",
    {
        "DbUser": str,
        "DbPassword": str,
    },
    total=False,
)


class UpdateRdsDbInstanceRequestRequestTypeDef(
    _RequiredUpdateRdsDbInstanceRequestRequestTypeDef,
    _OptionalUpdateRdsDbInstanceRequestRequestTypeDef,
):
    pass


_RequiredUpdateStackRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalUpdateStackRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStackRequestRequestTypeDef",
    {
        "Name": str,
        "Attributes": Mapping[Literal["Color"], str],
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": "StackConfigurationManagerTypeDef",
        "ChefConfiguration": "ChefConfigurationTypeDef",
        "UseCustomCookbooks": bool,
        "CustomCookbooksSource": "SourceTypeDef",
        "DefaultSshKeyName": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "UseOpsworksSecurityGroups": bool,
        "AgentVersion": str,
    },
    total=False,
)


class UpdateStackRequestRequestTypeDef(
    _RequiredUpdateStackRequestRequestTypeDef, _OptionalUpdateStackRequestRequestTypeDef
):
    pass


_RequiredUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserProfileRequestRequestTypeDef",
    {
        "IamUserArn": str,
    },
)
_OptionalUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserProfileRequestRequestTypeDef",
    {
        "SshUsername": str,
        "SshPublicKey": str,
        "AllowSelfManagement": bool,
    },
    total=False,
)


class UpdateUserProfileRequestRequestTypeDef(
    _RequiredUpdateUserProfileRequestRequestTypeDef, _OptionalUpdateUserProfileRequestRequestTypeDef
):
    pass


_RequiredUpdateVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)
_OptionalUpdateVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVolumeRequestRequestTypeDef",
    {
        "Name": str,
        "MountPoint": str,
    },
    total=False,
)


class UpdateVolumeRequestRequestTypeDef(
    _RequiredUpdateVolumeRequestRequestTypeDef, _OptionalUpdateVolumeRequestRequestTypeDef
):
    pass


UserProfileTypeDef = TypedDict(
    "UserProfileTypeDef",
    {
        "IamUserArn": str,
        "Name": str,
        "SshUsername": str,
        "SshPublicKey": str,
        "AllowSelfManagement": bool,
    },
    total=False,
)

_RequiredVolumeConfigurationTypeDef = TypedDict(
    "_RequiredVolumeConfigurationTypeDef",
    {
        "MountPoint": str,
        "NumberOfDisks": int,
        "Size": int,
    },
)
_OptionalVolumeConfigurationTypeDef = TypedDict(
    "_OptionalVolumeConfigurationTypeDef",
    {
        "RaidLevel": int,
        "VolumeType": str,
        "Iops": int,
        "Encrypted": bool,
    },
    total=False,
)


class VolumeConfigurationTypeDef(
    _RequiredVolumeConfigurationTypeDef, _OptionalVolumeConfigurationTypeDef
):
    pass


VolumeTypeDef = TypedDict(
    "VolumeTypeDef",
    {
        "VolumeId": str,
        "Ec2VolumeId": str,
        "Name": str,
        "RaidArrayId": str,
        "InstanceId": str,
        "Status": str,
        "Size": int,
        "Device": str,
        "MountPoint": str,
        "Region": str,
        "AvailabilityZone": str,
        "VolumeType": str,
        "Iops": int,
        "Encrypted": bool,
    },
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

WeeklyAutoScalingScheduleTypeDef = TypedDict(
    "WeeklyAutoScalingScheduleTypeDef",
    {
        "Monday": Dict[str, str],
        "Tuesday": Dict[str, str],
        "Wednesday": Dict[str, str],
        "Thursday": Dict[str, str],
        "Friday": Dict[str, str],
        "Saturday": Dict[str, str],
        "Sunday": Dict[str, str],
    },
    total=False,
)
