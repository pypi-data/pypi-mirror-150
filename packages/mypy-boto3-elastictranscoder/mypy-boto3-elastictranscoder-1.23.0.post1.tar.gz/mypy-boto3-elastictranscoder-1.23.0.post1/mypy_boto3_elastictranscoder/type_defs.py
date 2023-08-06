"""
Type annotations for elastictranscoder service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/type_defs/)

Usage::

    ```python
    from mypy_boto3_elastictranscoder.type_defs import ArtworkTypeDef

    data: ArtworkTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ArtworkTypeDef",
    "AudioCodecOptionsTypeDef",
    "AudioParametersTypeDef",
    "CancelJobRequestRequestTypeDef",
    "CaptionFormatTypeDef",
    "CaptionSourceTypeDef",
    "CaptionsTypeDef",
    "ClipTypeDef",
    "CreateJobOutputTypeDef",
    "CreateJobPlaylistTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobResponseTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "CreatePipelineResponseTypeDef",
    "CreatePresetRequestRequestTypeDef",
    "CreatePresetResponseTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "DeletePresetRequestRequestTypeDef",
    "DetectedPropertiesTypeDef",
    "EncryptionTypeDef",
    "HlsContentProtectionTypeDef",
    "InputCaptionsTypeDef",
    "JobAlbumArtTypeDef",
    "JobInputTypeDef",
    "JobOutputTypeDef",
    "JobTypeDef",
    "JobWatermarkTypeDef",
    "ListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef",
    "ListJobsByPipelineRequestRequestTypeDef",
    "ListJobsByPipelineResponseTypeDef",
    "ListJobsByStatusRequestListJobsByStatusPaginateTypeDef",
    "ListJobsByStatusRequestRequestTypeDef",
    "ListJobsByStatusResponseTypeDef",
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListPresetsRequestListPresetsPaginateTypeDef",
    "ListPresetsRequestRequestTypeDef",
    "ListPresetsResponseTypeDef",
    "NotificationsTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionTypeDef",
    "PipelineOutputConfigTypeDef",
    "PipelineTypeDef",
    "PlayReadyDrmTypeDef",
    "PlaylistTypeDef",
    "PresetTypeDef",
    "PresetWatermarkTypeDef",
    "ReadJobRequestJobCompleteWaitTypeDef",
    "ReadJobRequestRequestTypeDef",
    "ReadJobResponseTypeDef",
    "ReadPipelineRequestRequestTypeDef",
    "ReadPipelineResponseTypeDef",
    "ReadPresetRequestRequestTypeDef",
    "ReadPresetResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TestRoleRequestRequestTypeDef",
    "TestRoleResponseTypeDef",
    "ThumbnailsTypeDef",
    "TimeSpanTypeDef",
    "TimingTypeDef",
    "UpdatePipelineNotificationsRequestRequestTypeDef",
    "UpdatePipelineNotificationsResponseTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "UpdatePipelineResponseTypeDef",
    "UpdatePipelineStatusRequestRequestTypeDef",
    "UpdatePipelineStatusResponseTypeDef",
    "VideoParametersTypeDef",
    "WaiterConfigTypeDef",
    "WarningTypeDef",
)

ArtworkTypeDef = TypedDict(
    "ArtworkTypeDef",
    {
        "InputKey": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "SizingPolicy": str,
        "PaddingPolicy": str,
        "AlbumArtFormat": str,
        "Encryption": "EncryptionTypeDef",
    },
    total=False,
)

AudioCodecOptionsTypeDef = TypedDict(
    "AudioCodecOptionsTypeDef",
    {
        "Profile": str,
        "BitDepth": str,
        "BitOrder": str,
        "Signed": str,
    },
    total=False,
)

AudioParametersTypeDef = TypedDict(
    "AudioParametersTypeDef",
    {
        "Codec": str,
        "SampleRate": str,
        "BitRate": str,
        "Channels": str,
        "AudioPackingMode": str,
        "CodecOptions": "AudioCodecOptionsTypeDef",
    },
    total=False,
)

CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "Id": str,
    },
)

CaptionFormatTypeDef = TypedDict(
    "CaptionFormatTypeDef",
    {
        "Format": str,
        "Pattern": str,
        "Encryption": "EncryptionTypeDef",
    },
    total=False,
)

CaptionSourceTypeDef = TypedDict(
    "CaptionSourceTypeDef",
    {
        "Key": str,
        "Language": str,
        "TimeOffset": str,
        "Label": str,
        "Encryption": "EncryptionTypeDef",
    },
    total=False,
)

CaptionsTypeDef = TypedDict(
    "CaptionsTypeDef",
    {
        "MergePolicy": str,
        "CaptionSources": Sequence["CaptionSourceTypeDef"],
        "CaptionFormats": Sequence["CaptionFormatTypeDef"],
    },
    total=False,
)

ClipTypeDef = TypedDict(
    "ClipTypeDef",
    {
        "TimeSpan": "TimeSpanTypeDef",
    },
    total=False,
)

CreateJobOutputTypeDef = TypedDict(
    "CreateJobOutputTypeDef",
    {
        "Key": str,
        "ThumbnailPattern": str,
        "ThumbnailEncryption": "EncryptionTypeDef",
        "Rotate": str,
        "PresetId": str,
        "SegmentDuration": str,
        "Watermarks": Sequence["JobWatermarkTypeDef"],
        "AlbumArt": "JobAlbumArtTypeDef",
        "Composition": Sequence["ClipTypeDef"],
        "Captions": "CaptionsTypeDef",
        "Encryption": "EncryptionTypeDef",
    },
    total=False,
)

CreateJobPlaylistTypeDef = TypedDict(
    "CreateJobPlaylistTypeDef",
    {
        "Name": str,
        "Format": str,
        "OutputKeys": Sequence[str],
        "HlsContentProtection": "HlsContentProtectionTypeDef",
        "PlayReadyDrm": "PlayReadyDrmTypeDef",
    },
    total=False,
)

_RequiredCreateJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobRequestRequestTypeDef",
    {
        "PipelineId": str,
    },
)
_OptionalCreateJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobRequestRequestTypeDef",
    {
        "Input": "JobInputTypeDef",
        "Inputs": Sequence["JobInputTypeDef"],
        "Output": "CreateJobOutputTypeDef",
        "Outputs": Sequence["CreateJobOutputTypeDef"],
        "OutputKeyPrefix": str,
        "Playlists": Sequence["CreateJobPlaylistTypeDef"],
        "UserMetadata": Mapping[str, str],
    },
    total=False,
)


class CreateJobRequestRequestTypeDef(
    _RequiredCreateJobRequestRequestTypeDef, _OptionalCreateJobRequestRequestTypeDef
):
    pass


CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Job": "JobTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePipelineRequestRequestTypeDef",
    {
        "Name": str,
        "InputBucket": str,
        "Role": str,
    },
)
_OptionalCreatePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePipelineRequestRequestTypeDef",
    {
        "OutputBucket": str,
        "AwsKmsKeyArn": str,
        "Notifications": "NotificationsTypeDef",
        "ContentConfig": "PipelineOutputConfigTypeDef",
        "ThumbnailConfig": "PipelineOutputConfigTypeDef",
    },
    total=False,
)


class CreatePipelineRequestRequestTypeDef(
    _RequiredCreatePipelineRequestRequestTypeDef, _OptionalCreatePipelineRequestRequestTypeDef
):
    pass


CreatePipelineResponseTypeDef = TypedDict(
    "CreatePipelineResponseTypeDef",
    {
        "Pipeline": "PipelineTypeDef",
        "Warnings": List["WarningTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePresetRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePresetRequestRequestTypeDef",
    {
        "Name": str,
        "Container": str,
    },
)
_OptionalCreatePresetRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePresetRequestRequestTypeDef",
    {
        "Description": str,
        "Video": "VideoParametersTypeDef",
        "Audio": "AudioParametersTypeDef",
        "Thumbnails": "ThumbnailsTypeDef",
    },
    total=False,
)


class CreatePresetRequestRequestTypeDef(
    _RequiredCreatePresetRequestRequestTypeDef, _OptionalCreatePresetRequestRequestTypeDef
):
    pass


CreatePresetResponseTypeDef = TypedDict(
    "CreatePresetResponseTypeDef",
    {
        "Preset": "PresetTypeDef",
        "Warning": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeletePipelineRequestRequestTypeDef = TypedDict(
    "DeletePipelineRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeletePresetRequestRequestTypeDef = TypedDict(
    "DeletePresetRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DetectedPropertiesTypeDef = TypedDict(
    "DetectedPropertiesTypeDef",
    {
        "Width": int,
        "Height": int,
        "FrameRate": str,
        "FileSize": int,
        "DurationMillis": int,
    },
    total=False,
)

EncryptionTypeDef = TypedDict(
    "EncryptionTypeDef",
    {
        "Mode": str,
        "Key": str,
        "KeyMd5": str,
        "InitializationVector": str,
    },
    total=False,
)

HlsContentProtectionTypeDef = TypedDict(
    "HlsContentProtectionTypeDef",
    {
        "Method": str,
        "Key": str,
        "KeyMd5": str,
        "InitializationVector": str,
        "LicenseAcquisitionUrl": str,
        "KeyStoragePolicy": str,
    },
    total=False,
)

InputCaptionsTypeDef = TypedDict(
    "InputCaptionsTypeDef",
    {
        "MergePolicy": str,
        "CaptionSources": Sequence["CaptionSourceTypeDef"],
    },
    total=False,
)

JobAlbumArtTypeDef = TypedDict(
    "JobAlbumArtTypeDef",
    {
        "MergePolicy": str,
        "Artwork": Sequence["ArtworkTypeDef"],
    },
    total=False,
)

JobInputTypeDef = TypedDict(
    "JobInputTypeDef",
    {
        "Key": str,
        "FrameRate": str,
        "Resolution": str,
        "AspectRatio": str,
        "Interlaced": str,
        "Container": str,
        "Encryption": "EncryptionTypeDef",
        "TimeSpan": "TimeSpanTypeDef",
        "InputCaptions": "InputCaptionsTypeDef",
        "DetectedProperties": "DetectedPropertiesTypeDef",
    },
    total=False,
)

JobOutputTypeDef = TypedDict(
    "JobOutputTypeDef",
    {
        "Id": str,
        "Key": str,
        "ThumbnailPattern": str,
        "ThumbnailEncryption": "EncryptionTypeDef",
        "Rotate": str,
        "PresetId": str,
        "SegmentDuration": str,
        "Status": str,
        "StatusDetail": str,
        "Duration": int,
        "Width": int,
        "Height": int,
        "FrameRate": str,
        "FileSize": int,
        "DurationMillis": int,
        "Watermarks": List["JobWatermarkTypeDef"],
        "AlbumArt": "JobAlbumArtTypeDef",
        "Composition": List["ClipTypeDef"],
        "Captions": "CaptionsTypeDef",
        "Encryption": "EncryptionTypeDef",
        "AppliedColorSpaceConversion": str,
    },
    total=False,
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "Id": str,
        "Arn": str,
        "PipelineId": str,
        "Input": "JobInputTypeDef",
        "Inputs": List["JobInputTypeDef"],
        "Output": "JobOutputTypeDef",
        "Outputs": List["JobOutputTypeDef"],
        "OutputKeyPrefix": str,
        "Playlists": List["PlaylistTypeDef"],
        "Status": str,
        "UserMetadata": Dict[str, str],
        "Timing": "TimingTypeDef",
    },
    total=False,
)

JobWatermarkTypeDef = TypedDict(
    "JobWatermarkTypeDef",
    {
        "PresetWatermarkId": str,
        "InputKey": str,
        "Encryption": "EncryptionTypeDef",
    },
    total=False,
)

_RequiredListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef = TypedDict(
    "_RequiredListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef",
    {
        "PipelineId": str,
    },
)
_OptionalListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef = TypedDict(
    "_OptionalListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef",
    {
        "Ascending": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef(
    _RequiredListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef,
    _OptionalListJobsByPipelineRequestListJobsByPipelinePaginateTypeDef,
):
    pass


_RequiredListJobsByPipelineRequestRequestTypeDef = TypedDict(
    "_RequiredListJobsByPipelineRequestRequestTypeDef",
    {
        "PipelineId": str,
    },
)
_OptionalListJobsByPipelineRequestRequestTypeDef = TypedDict(
    "_OptionalListJobsByPipelineRequestRequestTypeDef",
    {
        "Ascending": str,
        "PageToken": str,
    },
    total=False,
)


class ListJobsByPipelineRequestRequestTypeDef(
    _RequiredListJobsByPipelineRequestRequestTypeDef,
    _OptionalListJobsByPipelineRequestRequestTypeDef,
):
    pass


ListJobsByPipelineResponseTypeDef = TypedDict(
    "ListJobsByPipelineResponseTypeDef",
    {
        "Jobs": List["JobTypeDef"],
        "NextPageToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListJobsByStatusRequestListJobsByStatusPaginateTypeDef = TypedDict(
    "_RequiredListJobsByStatusRequestListJobsByStatusPaginateTypeDef",
    {
        "Status": str,
    },
)
_OptionalListJobsByStatusRequestListJobsByStatusPaginateTypeDef = TypedDict(
    "_OptionalListJobsByStatusRequestListJobsByStatusPaginateTypeDef",
    {
        "Ascending": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListJobsByStatusRequestListJobsByStatusPaginateTypeDef(
    _RequiredListJobsByStatusRequestListJobsByStatusPaginateTypeDef,
    _OptionalListJobsByStatusRequestListJobsByStatusPaginateTypeDef,
):
    pass


_RequiredListJobsByStatusRequestRequestTypeDef = TypedDict(
    "_RequiredListJobsByStatusRequestRequestTypeDef",
    {
        "Status": str,
    },
)
_OptionalListJobsByStatusRequestRequestTypeDef = TypedDict(
    "_OptionalListJobsByStatusRequestRequestTypeDef",
    {
        "Ascending": str,
        "PageToken": str,
    },
    total=False,
)


class ListJobsByStatusRequestRequestTypeDef(
    _RequiredListJobsByStatusRequestRequestTypeDef, _OptionalListJobsByStatusRequestRequestTypeDef
):
    pass


ListJobsByStatusResponseTypeDef = TypedDict(
    "ListJobsByStatusResponseTypeDef",
    {
        "Jobs": List["JobTypeDef"],
        "NextPageToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelinesRequestListPipelinesPaginateTypeDef = TypedDict(
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    {
        "Ascending": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPipelinesRequestRequestTypeDef = TypedDict(
    "ListPipelinesRequestRequestTypeDef",
    {
        "Ascending": str,
        "PageToken": str,
    },
    total=False,
)

ListPipelinesResponseTypeDef = TypedDict(
    "ListPipelinesResponseTypeDef",
    {
        "Pipelines": List["PipelineTypeDef"],
        "NextPageToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPresetsRequestListPresetsPaginateTypeDef = TypedDict(
    "ListPresetsRequestListPresetsPaginateTypeDef",
    {
        "Ascending": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPresetsRequestRequestTypeDef = TypedDict(
    "ListPresetsRequestRequestTypeDef",
    {
        "Ascending": str,
        "PageToken": str,
    },
    total=False,
)

ListPresetsResponseTypeDef = TypedDict(
    "ListPresetsResponseTypeDef",
    {
        "Presets": List["PresetTypeDef"],
        "NextPageToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NotificationsTypeDef = TypedDict(
    "NotificationsTypeDef",
    {
        "Progressing": str,
        "Completed": str,
        "Warning": str,
        "Error": str,
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
        "GranteeType": str,
        "Grantee": str,
        "Access": Sequence[str],
    },
    total=False,
)

PipelineOutputConfigTypeDef = TypedDict(
    "PipelineOutputConfigTypeDef",
    {
        "Bucket": str,
        "StorageClass": str,
        "Permissions": Sequence["PermissionTypeDef"],
    },
    total=False,
)

PipelineTypeDef = TypedDict(
    "PipelineTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Status": str,
        "InputBucket": str,
        "OutputBucket": str,
        "Role": str,
        "AwsKmsKeyArn": str,
        "Notifications": "NotificationsTypeDef",
        "ContentConfig": "PipelineOutputConfigTypeDef",
        "ThumbnailConfig": "PipelineOutputConfigTypeDef",
    },
    total=False,
)

PlayReadyDrmTypeDef = TypedDict(
    "PlayReadyDrmTypeDef",
    {
        "Format": str,
        "Key": str,
        "KeyMd5": str,
        "KeyId": str,
        "InitializationVector": str,
        "LicenseAcquisitionUrl": str,
    },
    total=False,
)

PlaylistTypeDef = TypedDict(
    "PlaylistTypeDef",
    {
        "Name": str,
        "Format": str,
        "OutputKeys": List[str],
        "HlsContentProtection": "HlsContentProtectionTypeDef",
        "PlayReadyDrm": "PlayReadyDrmTypeDef",
        "Status": str,
        "StatusDetail": str,
    },
    total=False,
)

PresetTypeDef = TypedDict(
    "PresetTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "Container": str,
        "Audio": "AudioParametersTypeDef",
        "Video": "VideoParametersTypeDef",
        "Thumbnails": "ThumbnailsTypeDef",
        "Type": str,
    },
    total=False,
)

PresetWatermarkTypeDef = TypedDict(
    "PresetWatermarkTypeDef",
    {
        "Id": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "SizingPolicy": str,
        "HorizontalAlign": str,
        "HorizontalOffset": str,
        "VerticalAlign": str,
        "VerticalOffset": str,
        "Opacity": str,
        "Target": str,
    },
    total=False,
)

_RequiredReadJobRequestJobCompleteWaitTypeDef = TypedDict(
    "_RequiredReadJobRequestJobCompleteWaitTypeDef",
    {
        "Id": str,
    },
)
_OptionalReadJobRequestJobCompleteWaitTypeDef = TypedDict(
    "_OptionalReadJobRequestJobCompleteWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class ReadJobRequestJobCompleteWaitTypeDef(
    _RequiredReadJobRequestJobCompleteWaitTypeDef, _OptionalReadJobRequestJobCompleteWaitTypeDef
):
    pass


ReadJobRequestRequestTypeDef = TypedDict(
    "ReadJobRequestRequestTypeDef",
    {
        "Id": str,
    },
)

ReadJobResponseTypeDef = TypedDict(
    "ReadJobResponseTypeDef",
    {
        "Job": "JobTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReadPipelineRequestRequestTypeDef = TypedDict(
    "ReadPipelineRequestRequestTypeDef",
    {
        "Id": str,
    },
)

ReadPipelineResponseTypeDef = TypedDict(
    "ReadPipelineResponseTypeDef",
    {
        "Pipeline": "PipelineTypeDef",
        "Warnings": List["WarningTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReadPresetRequestRequestTypeDef = TypedDict(
    "ReadPresetRequestRequestTypeDef",
    {
        "Id": str,
    },
)

ReadPresetResponseTypeDef = TypedDict(
    "ReadPresetResponseTypeDef",
    {
        "Preset": "PresetTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
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

TestRoleRequestRequestTypeDef = TypedDict(
    "TestRoleRequestRequestTypeDef",
    {
        "Role": str,
        "InputBucket": str,
        "OutputBucket": str,
        "Topics": Sequence[str],
    },
)

TestRoleResponseTypeDef = TypedDict(
    "TestRoleResponseTypeDef",
    {
        "Success": str,
        "Messages": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ThumbnailsTypeDef = TypedDict(
    "ThumbnailsTypeDef",
    {
        "Format": str,
        "Interval": str,
        "Resolution": str,
        "AspectRatio": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "SizingPolicy": str,
        "PaddingPolicy": str,
    },
    total=False,
)

TimeSpanTypeDef = TypedDict(
    "TimeSpanTypeDef",
    {
        "StartTime": str,
        "Duration": str,
    },
    total=False,
)

TimingTypeDef = TypedDict(
    "TimingTypeDef",
    {
        "SubmitTimeMillis": int,
        "StartTimeMillis": int,
        "FinishTimeMillis": int,
    },
    total=False,
)

UpdatePipelineNotificationsRequestRequestTypeDef = TypedDict(
    "UpdatePipelineNotificationsRequestRequestTypeDef",
    {
        "Id": str,
        "Notifications": "NotificationsTypeDef",
    },
)

UpdatePipelineNotificationsResponseTypeDef = TypedDict(
    "UpdatePipelineNotificationsResponseTypeDef",
    {
        "Pipeline": "PipelineTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdatePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePipelineRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdatePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePipelineRequestRequestTypeDef",
    {
        "Name": str,
        "InputBucket": str,
        "Role": str,
        "AwsKmsKeyArn": str,
        "Notifications": "NotificationsTypeDef",
        "ContentConfig": "PipelineOutputConfigTypeDef",
        "ThumbnailConfig": "PipelineOutputConfigTypeDef",
    },
    total=False,
)


class UpdatePipelineRequestRequestTypeDef(
    _RequiredUpdatePipelineRequestRequestTypeDef, _OptionalUpdatePipelineRequestRequestTypeDef
):
    pass


UpdatePipelineResponseTypeDef = TypedDict(
    "UpdatePipelineResponseTypeDef",
    {
        "Pipeline": "PipelineTypeDef",
        "Warnings": List["WarningTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePipelineStatusRequestRequestTypeDef = TypedDict(
    "UpdatePipelineStatusRequestRequestTypeDef",
    {
        "Id": str,
        "Status": str,
    },
)

UpdatePipelineStatusResponseTypeDef = TypedDict(
    "UpdatePipelineStatusResponseTypeDef",
    {
        "Pipeline": "PipelineTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

VideoParametersTypeDef = TypedDict(
    "VideoParametersTypeDef",
    {
        "Codec": str,
        "CodecOptions": Mapping[str, str],
        "KeyframesMaxDist": str,
        "FixedGOP": str,
        "BitRate": str,
        "FrameRate": str,
        "MaxFrameRate": str,
        "Resolution": str,
        "AspectRatio": str,
        "MaxWidth": str,
        "MaxHeight": str,
        "DisplayAspectRatio": str,
        "SizingPolicy": str,
        "PaddingPolicy": str,
        "Watermarks": Sequence["PresetWatermarkTypeDef"],
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

WarningTypeDef = TypedDict(
    "WarningTypeDef",
    {
        "Code": str,
        "Message": str,
    },
    total=False,
)
