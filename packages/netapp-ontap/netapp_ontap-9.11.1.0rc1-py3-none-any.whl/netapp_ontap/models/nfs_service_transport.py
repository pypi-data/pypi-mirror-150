r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NfsServiceTransport", "NfsServiceTransportSchema"]
__pdoc__ = {
    "NfsServiceTransportSchema.resource": False,
    "NfsServiceTransportSchema.opts": False,
    "NfsServiceTransport": False,
}


class NfsServiceTransportSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsServiceTransport object"""

    tcp_enabled = fields.Boolean(data_key="tcp_enabled")
    r""" Specifies whether TCP transports are enabled on the server. """

    tcp_max_transfer_size = Size(data_key="tcp_max_transfer_size")
    r""" Specifies the maximum transfer size in bytes, that the storage system negotiates with the client for TCP transport of data for NFSv3 and NFSv4.x protocols. The range is 8192 to 1048576.

Example: 16384 """

    udp_enabled = fields.Boolean(data_key="udp_enabled")
    r""" Specifies whether UDP transports are enabled on the server. """

    @property
    def resource(self):
        return NfsServiceTransport

    gettable_fields = [
        "tcp_enabled",
        "tcp_max_transfer_size",
        "udp_enabled",
    ]
    """tcp_enabled,tcp_max_transfer_size,udp_enabled,"""

    patchable_fields = [
        "tcp_enabled",
        "tcp_max_transfer_size",
        "udp_enabled",
    ]
    """tcp_enabled,tcp_max_transfer_size,udp_enabled,"""

    postable_fields = [
        "tcp_enabled",
        "tcp_max_transfer_size",
        "udp_enabled",
    ]
    """tcp_enabled,tcp_max_transfer_size,udp_enabled,"""


class NfsServiceTransport(Resource):

    _schema = NfsServiceTransportSchema
