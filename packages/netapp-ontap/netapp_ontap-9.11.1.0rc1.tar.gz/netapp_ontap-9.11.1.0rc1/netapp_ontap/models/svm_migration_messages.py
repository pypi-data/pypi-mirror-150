r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationMessages", "SvmMigrationMessagesSchema"]
__pdoc__ = {
    "SvmMigrationMessagesSchema.resource": False,
    "SvmMigrationMessagesSchema.opts": False,
    "SvmMigrationMessages": False,
}


class SvmMigrationMessagesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationMessages object"""

    code = Size(data_key="code")
    r""" Message code """

    message = fields.Str(data_key="message")
    r""" Detailed message of warning or error. """

    @property
    def resource(self):
        return SvmMigrationMessages

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


class SvmMigrationMessages(Resource):

    _schema = SvmMigrationMessagesSchema
