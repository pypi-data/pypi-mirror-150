"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class S3Path(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    BUCKET_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    bucket: typing.Text
    key: typing.Text
    def __init__(self,
        *,
        bucket: typing.Text = ...,
        key: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["bucket",b"bucket","key",b"key"]) -> None: ...
global___S3Path = S3Path
