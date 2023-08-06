r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterDiagDetails", "MetroclusterDiagDetailsSchema"]
__pdoc__ = {
    "MetroclusterDiagDetailsSchema.resource": False,
    "MetroclusterDiagDetailsSchema.opts": False,
    "MetroclusterDiagDetails": False,
}


class MetroclusterDiagDetailsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDiagDetails object"""

    aggregate = fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, data_key="aggregate")
    r""" The aggregate field of the metrocluster_diag_details. """

    checks = fields.List(fields.Nested("netapp_ontap.models.metrocluster_diag_check.MetroclusterDiagCheckSchema", unknown=EXCLUDE), data_key="checks")
    r""" Collection of MetroCluster checks done for component. """

    cluster = fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", unknown=EXCLUDE, data_key="cluster")
    r""" The cluster field of the metrocluster_diag_details. """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node")
    r""" The node field of the metrocluster_diag_details. """

    timestamp = ImpreciseDateTime(data_key="timestamp")
    r""" Time check was done.

Example: 2016-03-10T14:35:16-08:00 """

    @property
    def resource(self):
        return MetroclusterDiagDetails

    gettable_fields = [
        "aggregate.links",
        "aggregate.name",
        "aggregate.uuid",
        "checks",
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "node.links",
        "node.name",
        "node.uuid",
        "timestamp",
    ]
    """aggregate.links,aggregate.name,aggregate.uuid,checks,cluster.links,cluster.name,cluster.uuid,node.links,node.name,node.uuid,timestamp,"""

    patchable_fields = [
        "aggregate.links",
        "aggregate.name",
        "aggregate.uuid",
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "node.name",
        "node.uuid",
    ]
    """aggregate.links,aggregate.name,aggregate.uuid,cluster.links,cluster.name,cluster.uuid,node.name,node.uuid,"""

    postable_fields = [
        "aggregate.links",
        "aggregate.name",
        "aggregate.uuid",
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "node.name",
        "node.uuid",
    ]
    """aggregate.links,aggregate.name,aggregate.uuid,cluster.links,cluster.name,cluster.uuid,node.name,node.uuid,"""


class MetroclusterDiagDetails(Resource):

    _schema = MetroclusterDiagDetailsSchema
