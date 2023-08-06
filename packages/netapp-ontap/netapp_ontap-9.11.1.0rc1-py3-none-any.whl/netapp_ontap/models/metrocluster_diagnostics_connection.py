r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterDiagnosticsConnection", "MetroclusterDiagnosticsConnectionSchema"]
__pdoc__ = {
    "MetroclusterDiagnosticsConnectionSchema.resource": False,
    "MetroclusterDiagnosticsConnectionSchema.opts": False,
    "MetroclusterDiagnosticsConnection": False,
}


class MetroclusterDiagnosticsConnectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDiagnosticsConnection object"""

    state = fields.Str(data_key="state")
    r""" Status of diagnostic operation for this component.

Valid choices:

* ok
* warning
* not_run
* not_applicable """

    summary = fields.Nested("netapp_ontap.models.error_arguments.ErrorArgumentsSchema", unknown=EXCLUDE, data_key="summary")
    r""" The summary field of the metrocluster_diagnostics_connection. """

    timestamp = ImpreciseDateTime(data_key="timestamp")
    r""" Time of the most recent diagnostic operation for this component

Example: 2016-03-10T14:35:16-08:00 """

    @property
    def resource(self):
        return MetroclusterDiagnosticsConnection

    gettable_fields = [
        "state",
        "summary",
        "timestamp",
    ]
    """state,summary,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class MetroclusterDiagnosticsConnection(Resource):

    _schema = MetroclusterDiagnosticsConnectionSchema
