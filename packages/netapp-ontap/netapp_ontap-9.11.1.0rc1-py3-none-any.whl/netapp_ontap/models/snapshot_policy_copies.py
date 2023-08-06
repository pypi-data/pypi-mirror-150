r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapshotPolicyCopies", "SnapshotPolicyCopiesSchema"]
__pdoc__ = {
    "SnapshotPolicyCopiesSchema.resource": False,
    "SnapshotPolicyCopiesSchema.opts": False,
    "SnapshotPolicyCopies": False,
}


class SnapshotPolicyCopiesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapshotPolicyCopies object"""

    count = Size(data_key="count")
    r""" The number of Snapshot copies to maintain for this schedule. """

    prefix = fields.Str(data_key="prefix")
    r""" The prefix to use while creating Snapshot copies at regular intervals. """

    schedule = fields.Nested("netapp_ontap.models.snapshot_policy_copies_schedule.SnapshotPolicyCopiesScheduleSchema", unknown=EXCLUDE, data_key="schedule")
    r""" The schedule field of the snapshot_policy_copies. """

    snapmirror_label = fields.Str(data_key="snapmirror_label")
    r""" Label for SnapMirror operations """

    @property
    def resource(self):
        return SnapshotPolicyCopies

    gettable_fields = [
        "count",
        "prefix",
        "schedule",
        "snapmirror_label",
    ]
    """count,prefix,schedule,snapmirror_label,"""

    patchable_fields = [
        "count",
        "prefix",
        "schedule",
        "snapmirror_label",
    ]
    """count,prefix,schedule,snapmirror_label,"""

    postable_fields = [
        "count",
        "prefix",
        "schedule",
        "snapmirror_label",
    ]
    """count,prefix,schedule,snapmirror_label,"""


class SnapshotPolicyCopies(Resource):

    _schema = SnapshotPolicyCopiesSchema
