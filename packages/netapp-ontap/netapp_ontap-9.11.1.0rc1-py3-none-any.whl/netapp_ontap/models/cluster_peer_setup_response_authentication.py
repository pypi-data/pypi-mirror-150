r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterPeerSetupResponseAuthentication", "ClusterPeerSetupResponseAuthenticationSchema"]
__pdoc__ = {
    "ClusterPeerSetupResponseAuthenticationSchema.resource": False,
    "ClusterPeerSetupResponseAuthenticationSchema.opts": False,
    "ClusterPeerSetupResponseAuthentication": False,
}


class ClusterPeerSetupResponseAuthenticationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterPeerSetupResponseAuthentication object"""

    expiry_time = ImpreciseDateTime(data_key="expiry_time")
    r""" The date and time the passphrase will expire.  The default expiry time is one hour.

Example: 2017-01-25T11:20:13Z """

    passphrase = fields.Str(data_key="passphrase")
    r""" A password to authenticate the cluster peer relationship. """

    @property
    def resource(self):
        return ClusterPeerSetupResponseAuthentication

    gettable_fields = [
        "expiry_time",
        "passphrase",
    ]
    """expiry_time,passphrase,"""

    patchable_fields = [
        "expiry_time",
        "passphrase",
    ]
    """expiry_time,passphrase,"""

    postable_fields = [
        "expiry_time",
        "passphrase",
    ]
    """expiry_time,passphrase,"""


class ClusterPeerSetupResponseAuthentication(Resource):

    _schema = ClusterPeerSetupResponseAuthenticationSchema
