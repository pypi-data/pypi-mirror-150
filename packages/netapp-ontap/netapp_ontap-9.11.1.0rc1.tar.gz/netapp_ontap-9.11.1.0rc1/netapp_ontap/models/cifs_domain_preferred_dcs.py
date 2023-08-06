r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsDomainPreferredDcs", "CifsDomainPreferredDcsSchema"]
__pdoc__ = {
    "CifsDomainPreferredDcsSchema.resource": False,
    "CifsDomainPreferredDcsSchema.opts": False,
    "CifsDomainPreferredDcs": False,
}


class CifsDomainPreferredDcsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsDomainPreferredDcs object"""

    fqdn = fields.Str(data_key="fqdn")
    r""" Fully Qualified Domain Name.


Example: test.com """

    server_ip = fields.Str(data_key="server_ip")
    r""" IP address of the preferred domain controller (DC). The address can be either an IPv4 or an IPv6 address.


Example: 4.4.4.4 """

    @property
    def resource(self):
        return CifsDomainPreferredDcs

    gettable_fields = [
        "fqdn",
        "server_ip",
    ]
    """fqdn,server_ip,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "fqdn",
        "server_ip",
    ]
    """fqdn,server_ip,"""


class CifsDomainPreferredDcs(Resource):

    _schema = CifsDomainPreferredDcsSchema
