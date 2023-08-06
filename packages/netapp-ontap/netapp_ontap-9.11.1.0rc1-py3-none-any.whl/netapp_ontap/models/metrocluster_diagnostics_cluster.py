r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterDiagnosticsCluster", "MetroclusterDiagnosticsClusterSchema"]
__pdoc__ = {
    "MetroclusterDiagnosticsClusterSchema.resource": False,
    "MetroclusterDiagnosticsClusterSchema.opts": False,
    "MetroclusterDiagnosticsCluster": False,
}


class MetroclusterDiagnosticsClusterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDiagnosticsCluster object"""

    state = fields.Str(data_key="state")
    r""" Status of diagnostic operation for this component.

Valid choices:

* ok
* warning
* not_run
* not_applicable """

    summary = fields.Nested("netapp_ontap.models.error_arguments.ErrorArgumentsSchema", unknown=EXCLUDE, data_key="summary")
    r""" The summary field of the metrocluster_diagnostics_cluster. """

    timestamp = ImpreciseDateTime(data_key="timestamp")
    r""" Time of the most recent diagnostic operation for this component

Example: 2016-03-10T14:35:16-08:00 """

    @property
    def resource(self):
        return MetroclusterDiagnosticsCluster

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


class MetroclusterDiagnosticsCluster(Resource):

    _schema = MetroclusterDiagnosticsClusterSchema
