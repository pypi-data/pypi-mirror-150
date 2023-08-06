r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3BucketProtectionStatusDestination", "S3BucketProtectionStatusDestinationSchema"]
__pdoc__ = {
    "S3BucketProtectionStatusDestinationSchema.resource": False,
    "S3BucketProtectionStatusDestinationSchema.opts": False,
    "S3BucketProtectionStatusDestination": False,
}


class S3BucketProtectionStatusDestinationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketProtectionStatusDestination object"""

    is_cloud = fields.Boolean(data_key="is_cloud")
    r""" Specifies whether a bucket is protected within the Cloud. """

    is_ontap = fields.Boolean(data_key="is_ontap")
    r""" Specifies whether a bucket is protected within ONTAP. """

    @property
    def resource(self):
        return S3BucketProtectionStatusDestination

    gettable_fields = [
        "is_cloud",
        "is_ontap",
    ]
    """is_cloud,is_ontap,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class S3BucketProtectionStatusDestination(Resource):

    _schema = S3BucketProtectionStatusDestinationSchema
