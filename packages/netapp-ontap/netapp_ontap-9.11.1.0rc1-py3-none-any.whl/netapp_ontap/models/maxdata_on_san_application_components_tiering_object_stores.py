r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MaxdataOnSanApplicationComponentsTieringObjectStores", "MaxdataOnSanApplicationComponentsTieringObjectStoresSchema"]
__pdoc__ = {
    "MaxdataOnSanApplicationComponentsTieringObjectStoresSchema.resource": False,
    "MaxdataOnSanApplicationComponentsTieringObjectStoresSchema.opts": False,
    "MaxdataOnSanApplicationComponentsTieringObjectStores": False,
}


class MaxdataOnSanApplicationComponentsTieringObjectStoresSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MaxdataOnSanApplicationComponentsTieringObjectStores object"""

    name = fields.Str(data_key="name")
    r""" The name of the object-store to use. """

    @property
    def resource(self):
        return MaxdataOnSanApplicationComponentsTieringObjectStores

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
    ]
    """name,"""


class MaxdataOnSanApplicationComponentsTieringObjectStores(Resource):

    _schema = MaxdataOnSanApplicationComponentsTieringObjectStoresSchema
