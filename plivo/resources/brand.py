# -*- coding: utf-8 -*-
from plivo.utils.validators import *

from ..base import ListResponseObject, PlivoResource, PlivoResourceInterface
from ..exceptions import *
from ..utils import *

class Brand(PlivoResource):
    _name = 'Brand'
    _identifier_string = 'brand_id'

class Brand(PlivoResourceInterface):
    _resource_type = Brand

    @validate_args(brand_id=[of_type(six.text_type)])
    def get(self, brand_id):
        return self.client.request(
            'GET', ('10dlc','Brand', brand_id), response_type=None)
            
    @validate_args(
        type=[optional(of_type(six.text_type))],
        status=[optional(of_type(six.text_type))])
    def list(self, type=None, status=None):
        return self.client.request(
            'GET', ('10dlc', 'Brand'),
            to_param_dict(self.list, locals()),
            response_type=None,
            objects_type=None)
    
    @validate_args(
        brand_alias=[optional(of_type(six.text_type))],
        brand_type=[optional(of_type(six.text_type))],
        profile_uuid=[optional(of_type(six.text_type))],
        secondary_vetting=[optional(of_type_exact(bool))],
        )
    def create(self,
               brand_alias,
               brand_type,
               profile_uuid,
               secondary_vetting,
               ):
        return self.client.request('POST', ('10dlc', 'Brand'),
                                   to_param_dict(self.create, locals()))