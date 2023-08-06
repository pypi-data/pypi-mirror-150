r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeIdcsScanner", "VolumeIdcsScannerSchema"]
__pdoc__ = {
    "VolumeIdcsScannerSchema.resource": False,
    "VolumeIdcsScannerSchema.opts": False,
    "VolumeIdcsScanner": False,
}


class VolumeIdcsScannerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeIdcsScanner object"""

    enabled = fields.Boolean(data_key="enabled")
    r""" Specifies the adminsitrative state of the inactive data compression scanner. """

    operation_state = fields.Str(data_key="operation_state")
    r""" Specifies the operational state of the inactive data compression scanner. VALID for PATCH and GET. Valid options for PATCH are "idle" and "active".

Valid choices:

* idle
* active """

    status = fields.Str(data_key="status")
    r""" Status of last inactive data compression scan on the volume.

Valid choices:

* success
* failure """

    threshold_inactive_time = ImpreciseDateTime(data_key="threshold_inactive_time")
    r""" Time interval after which inactive data compression will be triggered automatically.The value is in days and is represented in the ISO-8601 format as "P<num>D" , for example "P3D" represents a duration of 3 days. """

    @property
    def resource(self):
        return VolumeIdcsScanner

    gettable_fields = [
        "enabled",
        "operation_state",
        "status",
        "threshold_inactive_time",
    ]
    """enabled,operation_state,status,threshold_inactive_time,"""

    patchable_fields = [
        "operation_state",
    ]
    """operation_state,"""

    postable_fields = [
        "operation_state",
    ]
    """operation_state,"""


class VolumeIdcsScanner(Resource):

    _schema = VolumeIdcsScannerSchema
