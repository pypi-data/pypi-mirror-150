"""
Type annotations for groundstation service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/type_defs/)

Usage::

    ```python
    from mypy_boto3_groundstation.type_defs import AntennaDemodDecodeDetailsTypeDef

    data: AntennaDemodDecodeDetailsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AngleUnitsType,
    BandwidthUnitsType,
    ConfigCapabilityTypeType,
    ContactStatusType,
    CriticalityType,
    EndpointStatusType,
    FrequencyUnitsType,
    PolarizationType,
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
    "AntennaDemodDecodeDetailsTypeDef",
    "AntennaDownlinkConfigTypeDef",
    "AntennaDownlinkDemodDecodeConfigTypeDef",
    "AntennaUplinkConfigTypeDef",
    "CancelContactRequestRequestTypeDef",
    "ConfigDetailsTypeDef",
    "ConfigIdResponseTypeDef",
    "ConfigListItemTypeDef",
    "ConfigTypeDataTypeDef",
    "ContactDataTypeDef",
    "ContactIdResponseTypeDef",
    "CreateConfigRequestRequestTypeDef",
    "CreateDataflowEndpointGroupRequestRequestTypeDef",
    "CreateMissionProfileRequestRequestTypeDef",
    "DataflowDetailTypeDef",
    "DataflowEndpointConfigTypeDef",
    "DataflowEndpointGroupIdResponseTypeDef",
    "DataflowEndpointListItemTypeDef",
    "DataflowEndpointTypeDef",
    "DecodeConfigTypeDef",
    "DeleteConfigRequestRequestTypeDef",
    "DeleteDataflowEndpointGroupRequestRequestTypeDef",
    "DeleteMissionProfileRequestRequestTypeDef",
    "DemodulationConfigTypeDef",
    "DescribeContactRequestRequestTypeDef",
    "DescribeContactResponseTypeDef",
    "DestinationTypeDef",
    "EirpTypeDef",
    "ElevationTypeDef",
    "EndpointDetailsTypeDef",
    "FrequencyBandwidthTypeDef",
    "FrequencyTypeDef",
    "GetConfigRequestRequestTypeDef",
    "GetConfigResponseTypeDef",
    "GetDataflowEndpointGroupRequestRequestTypeDef",
    "GetDataflowEndpointGroupResponseTypeDef",
    "GetMinuteUsageRequestRequestTypeDef",
    "GetMinuteUsageResponseTypeDef",
    "GetMissionProfileRequestRequestTypeDef",
    "GetMissionProfileResponseTypeDef",
    "GetSatelliteRequestRequestTypeDef",
    "GetSatelliteResponseTypeDef",
    "GroundStationDataTypeDef",
    "ListConfigsRequestListConfigsPaginateTypeDef",
    "ListConfigsRequestRequestTypeDef",
    "ListConfigsResponseTypeDef",
    "ListContactsRequestListContactsPaginateTypeDef",
    "ListContactsRequestRequestTypeDef",
    "ListContactsResponseTypeDef",
    "ListDataflowEndpointGroupsRequestListDataflowEndpointGroupsPaginateTypeDef",
    "ListDataflowEndpointGroupsRequestRequestTypeDef",
    "ListDataflowEndpointGroupsResponseTypeDef",
    "ListGroundStationsRequestListGroundStationsPaginateTypeDef",
    "ListGroundStationsRequestRequestTypeDef",
    "ListGroundStationsResponseTypeDef",
    "ListMissionProfilesRequestListMissionProfilesPaginateTypeDef",
    "ListMissionProfilesRequestRequestTypeDef",
    "ListMissionProfilesResponseTypeDef",
    "ListSatellitesRequestListSatellitesPaginateTypeDef",
    "ListSatellitesRequestRequestTypeDef",
    "ListSatellitesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MissionProfileIdResponseTypeDef",
    "MissionProfileListItemTypeDef",
    "PaginatorConfigTypeDef",
    "ReserveContactRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "S3RecordingConfigTypeDef",
    "S3RecordingDetailsTypeDef",
    "SatelliteListItemTypeDef",
    "SecurityDetailsTypeDef",
    "SocketAddressTypeDef",
    "SourceTypeDef",
    "SpectrumConfigTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TrackingConfigTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConfigRequestRequestTypeDef",
    "UpdateMissionProfileRequestRequestTypeDef",
    "UplinkEchoConfigTypeDef",
    "UplinkSpectrumConfigTypeDef",
)

AntennaDemodDecodeDetailsTypeDef = TypedDict(
    "AntennaDemodDecodeDetailsTypeDef",
    {
        "outputNode": str,
    },
    total=False,
)

AntennaDownlinkConfigTypeDef = TypedDict(
    "AntennaDownlinkConfigTypeDef",
    {
        "spectrumConfig": "SpectrumConfigTypeDef",
    },
)

AntennaDownlinkDemodDecodeConfigTypeDef = TypedDict(
    "AntennaDownlinkDemodDecodeConfigTypeDef",
    {
        "decodeConfig": "DecodeConfigTypeDef",
        "demodulationConfig": "DemodulationConfigTypeDef",
        "spectrumConfig": "SpectrumConfigTypeDef",
    },
)

_RequiredAntennaUplinkConfigTypeDef = TypedDict(
    "_RequiredAntennaUplinkConfigTypeDef",
    {
        "spectrumConfig": "UplinkSpectrumConfigTypeDef",
        "targetEirp": "EirpTypeDef",
    },
)
_OptionalAntennaUplinkConfigTypeDef = TypedDict(
    "_OptionalAntennaUplinkConfigTypeDef",
    {
        "transmitDisabled": bool,
    },
    total=False,
)

class AntennaUplinkConfigTypeDef(
    _RequiredAntennaUplinkConfigTypeDef, _OptionalAntennaUplinkConfigTypeDef
):
    pass

CancelContactRequestRequestTypeDef = TypedDict(
    "CancelContactRequestRequestTypeDef",
    {
        "contactId": str,
    },
)

ConfigDetailsTypeDef = TypedDict(
    "ConfigDetailsTypeDef",
    {
        "antennaDemodDecodeDetails": "AntennaDemodDecodeDetailsTypeDef",
        "endpointDetails": "EndpointDetailsTypeDef",
        "s3RecordingDetails": "S3RecordingDetailsTypeDef",
    },
    total=False,
)

ConfigIdResponseTypeDef = TypedDict(
    "ConfigIdResponseTypeDef",
    {
        "configArn": str,
        "configId": str,
        "configType": ConfigCapabilityTypeType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ConfigListItemTypeDef = TypedDict(
    "ConfigListItemTypeDef",
    {
        "configArn": str,
        "configId": str,
        "configType": ConfigCapabilityTypeType,
        "name": str,
    },
    total=False,
)

ConfigTypeDataTypeDef = TypedDict(
    "ConfigTypeDataTypeDef",
    {
        "antennaDownlinkConfig": "AntennaDownlinkConfigTypeDef",
        "antennaDownlinkDemodDecodeConfig": "AntennaDownlinkDemodDecodeConfigTypeDef",
        "antennaUplinkConfig": "AntennaUplinkConfigTypeDef",
        "dataflowEndpointConfig": "DataflowEndpointConfigTypeDef",
        "s3RecordingConfig": "S3RecordingConfigTypeDef",
        "trackingConfig": "TrackingConfigTypeDef",
        "uplinkEchoConfig": "UplinkEchoConfigTypeDef",
    },
    total=False,
)

ContactDataTypeDef = TypedDict(
    "ContactDataTypeDef",
    {
        "contactId": str,
        "contactStatus": ContactStatusType,
        "endTime": datetime,
        "errorMessage": str,
        "groundStation": str,
        "maximumElevation": "ElevationTypeDef",
        "missionProfileArn": str,
        "postPassEndTime": datetime,
        "prePassStartTime": datetime,
        "region": str,
        "satelliteArn": str,
        "startTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

ContactIdResponseTypeDef = TypedDict(
    "ContactIdResponseTypeDef",
    {
        "contactId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConfigRequestRequestTypeDef",
    {
        "configData": "ConfigTypeDataTypeDef",
        "name": str,
    },
)
_OptionalCreateConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConfigRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateConfigRequestRequestTypeDef(
    _RequiredCreateConfigRequestRequestTypeDef, _OptionalCreateConfigRequestRequestTypeDef
):
    pass

_RequiredCreateDataflowEndpointGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataflowEndpointGroupRequestRequestTypeDef",
    {
        "endpointDetails": Sequence["EndpointDetailsTypeDef"],
    },
)
_OptionalCreateDataflowEndpointGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataflowEndpointGroupRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateDataflowEndpointGroupRequestRequestTypeDef(
    _RequiredCreateDataflowEndpointGroupRequestRequestTypeDef,
    _OptionalCreateDataflowEndpointGroupRequestRequestTypeDef,
):
    pass

_RequiredCreateMissionProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMissionProfileRequestRequestTypeDef",
    {
        "dataflowEdges": Sequence[Sequence[str]],
        "minimumViableContactDurationSeconds": int,
        "name": str,
        "trackingConfigArn": str,
    },
)
_OptionalCreateMissionProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMissionProfileRequestRequestTypeDef",
    {
        "contactPostPassDurationSeconds": int,
        "contactPrePassDurationSeconds": int,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateMissionProfileRequestRequestTypeDef(
    _RequiredCreateMissionProfileRequestRequestTypeDef,
    _OptionalCreateMissionProfileRequestRequestTypeDef,
):
    pass

DataflowDetailTypeDef = TypedDict(
    "DataflowDetailTypeDef",
    {
        "destination": "DestinationTypeDef",
        "errorMessage": str,
        "source": "SourceTypeDef",
    },
    total=False,
)

_RequiredDataflowEndpointConfigTypeDef = TypedDict(
    "_RequiredDataflowEndpointConfigTypeDef",
    {
        "dataflowEndpointName": str,
    },
)
_OptionalDataflowEndpointConfigTypeDef = TypedDict(
    "_OptionalDataflowEndpointConfigTypeDef",
    {
        "dataflowEndpointRegion": str,
    },
    total=False,
)

class DataflowEndpointConfigTypeDef(
    _RequiredDataflowEndpointConfigTypeDef, _OptionalDataflowEndpointConfigTypeDef
):
    pass

DataflowEndpointGroupIdResponseTypeDef = TypedDict(
    "DataflowEndpointGroupIdResponseTypeDef",
    {
        "dataflowEndpointGroupId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataflowEndpointListItemTypeDef = TypedDict(
    "DataflowEndpointListItemTypeDef",
    {
        "dataflowEndpointGroupArn": str,
        "dataflowEndpointGroupId": str,
    },
    total=False,
)

DataflowEndpointTypeDef = TypedDict(
    "DataflowEndpointTypeDef",
    {
        "address": "SocketAddressTypeDef",
        "mtu": int,
        "name": str,
        "status": EndpointStatusType,
    },
    total=False,
)

DecodeConfigTypeDef = TypedDict(
    "DecodeConfigTypeDef",
    {
        "unvalidatedJSON": str,
    },
)

DeleteConfigRequestRequestTypeDef = TypedDict(
    "DeleteConfigRequestRequestTypeDef",
    {
        "configId": str,
        "configType": ConfigCapabilityTypeType,
    },
)

DeleteDataflowEndpointGroupRequestRequestTypeDef = TypedDict(
    "DeleteDataflowEndpointGroupRequestRequestTypeDef",
    {
        "dataflowEndpointGroupId": str,
    },
)

DeleteMissionProfileRequestRequestTypeDef = TypedDict(
    "DeleteMissionProfileRequestRequestTypeDef",
    {
        "missionProfileId": str,
    },
)

DemodulationConfigTypeDef = TypedDict(
    "DemodulationConfigTypeDef",
    {
        "unvalidatedJSON": str,
    },
)

DescribeContactRequestRequestTypeDef = TypedDict(
    "DescribeContactRequestRequestTypeDef",
    {
        "contactId": str,
    },
)

DescribeContactResponseTypeDef = TypedDict(
    "DescribeContactResponseTypeDef",
    {
        "contactId": str,
        "contactStatus": ContactStatusType,
        "dataflowList": List["DataflowDetailTypeDef"],
        "endTime": datetime,
        "errorMessage": str,
        "groundStation": str,
        "maximumElevation": "ElevationTypeDef",
        "missionProfileArn": str,
        "postPassEndTime": datetime,
        "prePassStartTime": datetime,
        "region": str,
        "satelliteArn": str,
        "startTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "configDetails": "ConfigDetailsTypeDef",
        "configId": str,
        "configType": ConfigCapabilityTypeType,
        "dataflowDestinationRegion": str,
    },
    total=False,
)

EirpTypeDef = TypedDict(
    "EirpTypeDef",
    {
        "units": Literal["dBW"],
        "value": float,
    },
)

ElevationTypeDef = TypedDict(
    "ElevationTypeDef",
    {
        "unit": AngleUnitsType,
        "value": float,
    },
)

EndpointDetailsTypeDef = TypedDict(
    "EndpointDetailsTypeDef",
    {
        "endpoint": "DataflowEndpointTypeDef",
        "securityDetails": "SecurityDetailsTypeDef",
    },
    total=False,
)

FrequencyBandwidthTypeDef = TypedDict(
    "FrequencyBandwidthTypeDef",
    {
        "units": BandwidthUnitsType,
        "value": float,
    },
)

FrequencyTypeDef = TypedDict(
    "FrequencyTypeDef",
    {
        "units": FrequencyUnitsType,
        "value": float,
    },
)

GetConfigRequestRequestTypeDef = TypedDict(
    "GetConfigRequestRequestTypeDef",
    {
        "configId": str,
        "configType": ConfigCapabilityTypeType,
    },
)

GetConfigResponseTypeDef = TypedDict(
    "GetConfigResponseTypeDef",
    {
        "configArn": str,
        "configData": "ConfigTypeDataTypeDef",
        "configId": str,
        "configType": ConfigCapabilityTypeType,
        "name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDataflowEndpointGroupRequestRequestTypeDef = TypedDict(
    "GetDataflowEndpointGroupRequestRequestTypeDef",
    {
        "dataflowEndpointGroupId": str,
    },
)

GetDataflowEndpointGroupResponseTypeDef = TypedDict(
    "GetDataflowEndpointGroupResponseTypeDef",
    {
        "dataflowEndpointGroupArn": str,
        "dataflowEndpointGroupId": str,
        "endpointsDetails": List["EndpointDetailsTypeDef"],
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetMinuteUsageRequestRequestTypeDef = TypedDict(
    "GetMinuteUsageRequestRequestTypeDef",
    {
        "month": int,
        "year": int,
    },
)

GetMinuteUsageResponseTypeDef = TypedDict(
    "GetMinuteUsageResponseTypeDef",
    {
        "estimatedMinutesRemaining": int,
        "isReservedMinutesCustomer": bool,
        "totalReservedMinuteAllocation": int,
        "totalScheduledMinutes": int,
        "upcomingMinutesScheduled": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetMissionProfileRequestRequestTypeDef = TypedDict(
    "GetMissionProfileRequestRequestTypeDef",
    {
        "missionProfileId": str,
    },
)

GetMissionProfileResponseTypeDef = TypedDict(
    "GetMissionProfileResponseTypeDef",
    {
        "contactPostPassDurationSeconds": int,
        "contactPrePassDurationSeconds": int,
        "dataflowEdges": List[List[str]],
        "minimumViableContactDurationSeconds": int,
        "missionProfileArn": str,
        "missionProfileId": str,
        "name": str,
        "region": str,
        "tags": Dict[str, str],
        "trackingConfigArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSatelliteRequestRequestTypeDef = TypedDict(
    "GetSatelliteRequestRequestTypeDef",
    {
        "satelliteId": str,
    },
)

GetSatelliteResponseTypeDef = TypedDict(
    "GetSatelliteResponseTypeDef",
    {
        "groundStations": List[str],
        "noradSatelliteID": int,
        "satelliteArn": str,
        "satelliteId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GroundStationDataTypeDef = TypedDict(
    "GroundStationDataTypeDef",
    {
        "groundStationId": str,
        "groundStationName": str,
        "region": str,
    },
    total=False,
)

ListConfigsRequestListConfigsPaginateTypeDef = TypedDict(
    "ListConfigsRequestListConfigsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListConfigsRequestRequestTypeDef = TypedDict(
    "ListConfigsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListConfigsResponseTypeDef = TypedDict(
    "ListConfigsResponseTypeDef",
    {
        "configList": List["ConfigListItemTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListContactsRequestListContactsPaginateTypeDef = TypedDict(
    "_RequiredListContactsRequestListContactsPaginateTypeDef",
    {
        "endTime": Union[datetime, str],
        "startTime": Union[datetime, str],
        "statusList": Sequence[ContactStatusType],
    },
)
_OptionalListContactsRequestListContactsPaginateTypeDef = TypedDict(
    "_OptionalListContactsRequestListContactsPaginateTypeDef",
    {
        "groundStation": str,
        "missionProfileArn": str,
        "satelliteArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListContactsRequestListContactsPaginateTypeDef(
    _RequiredListContactsRequestListContactsPaginateTypeDef,
    _OptionalListContactsRequestListContactsPaginateTypeDef,
):
    pass

_RequiredListContactsRequestRequestTypeDef = TypedDict(
    "_RequiredListContactsRequestRequestTypeDef",
    {
        "endTime": Union[datetime, str],
        "startTime": Union[datetime, str],
        "statusList": Sequence[ContactStatusType],
    },
)
_OptionalListContactsRequestRequestTypeDef = TypedDict(
    "_OptionalListContactsRequestRequestTypeDef",
    {
        "groundStation": str,
        "maxResults": int,
        "missionProfileArn": str,
        "nextToken": str,
        "satelliteArn": str,
    },
    total=False,
)

class ListContactsRequestRequestTypeDef(
    _RequiredListContactsRequestRequestTypeDef, _OptionalListContactsRequestRequestTypeDef
):
    pass

ListContactsResponseTypeDef = TypedDict(
    "ListContactsResponseTypeDef",
    {
        "contactList": List["ContactDataTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDataflowEndpointGroupsRequestListDataflowEndpointGroupsPaginateTypeDef = TypedDict(
    "ListDataflowEndpointGroupsRequestListDataflowEndpointGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDataflowEndpointGroupsRequestRequestTypeDef = TypedDict(
    "ListDataflowEndpointGroupsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListDataflowEndpointGroupsResponseTypeDef = TypedDict(
    "ListDataflowEndpointGroupsResponseTypeDef",
    {
        "dataflowEndpointGroupList": List["DataflowEndpointListItemTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListGroundStationsRequestListGroundStationsPaginateTypeDef = TypedDict(
    "ListGroundStationsRequestListGroundStationsPaginateTypeDef",
    {
        "satelliteId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListGroundStationsRequestRequestTypeDef = TypedDict(
    "ListGroundStationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "satelliteId": str,
    },
    total=False,
)

ListGroundStationsResponseTypeDef = TypedDict(
    "ListGroundStationsResponseTypeDef",
    {
        "groundStationList": List["GroundStationDataTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMissionProfilesRequestListMissionProfilesPaginateTypeDef = TypedDict(
    "ListMissionProfilesRequestListMissionProfilesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMissionProfilesRequestRequestTypeDef = TypedDict(
    "ListMissionProfilesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListMissionProfilesResponseTypeDef = TypedDict(
    "ListMissionProfilesResponseTypeDef",
    {
        "missionProfileList": List["MissionProfileListItemTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSatellitesRequestListSatellitesPaginateTypeDef = TypedDict(
    "ListSatellitesRequestListSatellitesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSatellitesRequestRequestTypeDef = TypedDict(
    "ListSatellitesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSatellitesResponseTypeDef = TypedDict(
    "ListSatellitesResponseTypeDef",
    {
        "nextToken": str,
        "satellites": List["SatelliteListItemTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MissionProfileIdResponseTypeDef = TypedDict(
    "MissionProfileIdResponseTypeDef",
    {
        "missionProfileId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MissionProfileListItemTypeDef = TypedDict(
    "MissionProfileListItemTypeDef",
    {
        "missionProfileArn": str,
        "missionProfileId": str,
        "name": str,
        "region": str,
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

_RequiredReserveContactRequestRequestTypeDef = TypedDict(
    "_RequiredReserveContactRequestRequestTypeDef",
    {
        "endTime": Union[datetime, str],
        "groundStation": str,
        "missionProfileArn": str,
        "satelliteArn": str,
        "startTime": Union[datetime, str],
    },
)
_OptionalReserveContactRequestRequestTypeDef = TypedDict(
    "_OptionalReserveContactRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class ReserveContactRequestRequestTypeDef(
    _RequiredReserveContactRequestRequestTypeDef, _OptionalReserveContactRequestRequestTypeDef
):
    pass

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

_RequiredS3RecordingConfigTypeDef = TypedDict(
    "_RequiredS3RecordingConfigTypeDef",
    {
        "bucketArn": str,
        "roleArn": str,
    },
)
_OptionalS3RecordingConfigTypeDef = TypedDict(
    "_OptionalS3RecordingConfigTypeDef",
    {
        "prefix": str,
    },
    total=False,
)

class S3RecordingConfigTypeDef(
    _RequiredS3RecordingConfigTypeDef, _OptionalS3RecordingConfigTypeDef
):
    pass

S3RecordingDetailsTypeDef = TypedDict(
    "S3RecordingDetailsTypeDef",
    {
        "bucketArn": str,
        "keyTemplate": str,
    },
    total=False,
)

SatelliteListItemTypeDef = TypedDict(
    "SatelliteListItemTypeDef",
    {
        "groundStations": List[str],
        "noradSatelliteID": int,
        "satelliteArn": str,
        "satelliteId": str,
    },
    total=False,
)

SecurityDetailsTypeDef = TypedDict(
    "SecurityDetailsTypeDef",
    {
        "roleArn": str,
        "securityGroupIds": Sequence[str],
        "subnetIds": Sequence[str],
    },
)

SocketAddressTypeDef = TypedDict(
    "SocketAddressTypeDef",
    {
        "name": str,
        "port": int,
    },
)

SourceTypeDef = TypedDict(
    "SourceTypeDef",
    {
        "configDetails": "ConfigDetailsTypeDef",
        "configId": str,
        "configType": ConfigCapabilityTypeType,
        "dataflowSourceRegion": str,
    },
    total=False,
)

_RequiredSpectrumConfigTypeDef = TypedDict(
    "_RequiredSpectrumConfigTypeDef",
    {
        "bandwidth": "FrequencyBandwidthTypeDef",
        "centerFrequency": "FrequencyTypeDef",
    },
)
_OptionalSpectrumConfigTypeDef = TypedDict(
    "_OptionalSpectrumConfigTypeDef",
    {
        "polarization": PolarizationType,
    },
    total=False,
)

class SpectrumConfigTypeDef(_RequiredSpectrumConfigTypeDef, _OptionalSpectrumConfigTypeDef):
    pass

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

TrackingConfigTypeDef = TypedDict(
    "TrackingConfigTypeDef",
    {
        "autotrack": CriticalityType,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateConfigRequestRequestTypeDef = TypedDict(
    "UpdateConfigRequestRequestTypeDef",
    {
        "configData": "ConfigTypeDataTypeDef",
        "configId": str,
        "configType": ConfigCapabilityTypeType,
        "name": str,
    },
)

_RequiredUpdateMissionProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMissionProfileRequestRequestTypeDef",
    {
        "missionProfileId": str,
    },
)
_OptionalUpdateMissionProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMissionProfileRequestRequestTypeDef",
    {
        "contactPostPassDurationSeconds": int,
        "contactPrePassDurationSeconds": int,
        "dataflowEdges": Sequence[Sequence[str]],
        "minimumViableContactDurationSeconds": int,
        "name": str,
        "trackingConfigArn": str,
    },
    total=False,
)

class UpdateMissionProfileRequestRequestTypeDef(
    _RequiredUpdateMissionProfileRequestRequestTypeDef,
    _OptionalUpdateMissionProfileRequestRequestTypeDef,
):
    pass

UplinkEchoConfigTypeDef = TypedDict(
    "UplinkEchoConfigTypeDef",
    {
        "antennaUplinkConfigArn": str,
        "enabled": bool,
    },
)

_RequiredUplinkSpectrumConfigTypeDef = TypedDict(
    "_RequiredUplinkSpectrumConfigTypeDef",
    {
        "centerFrequency": "FrequencyTypeDef",
    },
)
_OptionalUplinkSpectrumConfigTypeDef = TypedDict(
    "_OptionalUplinkSpectrumConfigTypeDef",
    {
        "polarization": PolarizationType,
    },
    total=False,
)

class UplinkSpectrumConfigTypeDef(
    _RequiredUplinkSpectrumConfigTypeDef, _OptionalUplinkSpectrumConfigTypeDef
):
    pass
