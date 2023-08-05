'''
# Encrypted Buckets

> A CDK construct for encrypted S3 Buckets.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_kms
import aws_cdk.aws_s3
import constructs


class EncryptedBucket(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="encrypted-bucket.EncryptedBucket",
):
    '''A CDK construct for encrypted S3 Buckets.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param versioned: Use S3 Versioning for bucket. Default: false
        '''
        props = EncryptedBucketProps(versioned=versioned)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        return typing.cast(aws_cdk.aws_s3.IBucket, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: aws_cdk.aws_s3.IBucket) -> None:
        jsii.set(self, "bucket", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> aws_cdk.aws_kms.IKey:
        return typing.cast(aws_cdk.aws_kms.IKey, jsii.get(self, "key"))

    @key.setter
    def key(self, value: aws_cdk.aws_kms.IKey) -> None:
        jsii.set(self, "key", value)


@jsii.data_type(
    jsii_type="encrypted-bucket.EncryptedBucketProps",
    jsii_struct_bases=[],
    name_mapping={"versioned": "versioned"},
)
class EncryptedBucketProps:
    def __init__(self, *, versioned: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param versioned: Use S3 Versioning for bucket. Default: false
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if versioned is not None:
            self._values["versioned"] = versioned

    @builtins.property
    def versioned(self) -> typing.Optional[builtins.bool]:
        '''Use S3 Versioning for bucket.

        :default: false
        '''
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptedBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EncryptedBucket",
    "EncryptedBucketProps",
]

publication.publish()
