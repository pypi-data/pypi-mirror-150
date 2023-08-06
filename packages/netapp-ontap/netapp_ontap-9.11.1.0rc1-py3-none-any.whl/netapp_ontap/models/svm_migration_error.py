r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationError", "SvmMigrationErrorSchema"]
__pdoc__ = {
    "SvmMigrationErrorSchema.resource": False,
    "SvmMigrationErrorSchema.opts": False,
    "SvmMigrationError": False,
}


class SvmMigrationErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationError object"""

    code = Size(data_key="code")
    r""" Message code """

    message = fields.Str(data_key="message")
    r""" Detailed message of warning or error. """

    @property
    def resource(self):
        return SvmMigrationError

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    postable_fields = [
        "code",
        "message",
    ]
    """code,message,"""


class SvmMigrationError(Resource):

    _schema = SvmMigrationErrorSchema
