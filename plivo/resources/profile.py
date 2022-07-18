# -*- coding: utf-8 -*-
from plivo.utils.validators import *

from ..base import ListResponseObject, PlivoResource, PlivoResourceInterface
from ..exceptions import *
from ..utils import *

class Profile(PlivoResource):
    _name = 'Profile'
    _identifier_string = 'Profile_uuid'

class Profile(PlivoResourceInterface):
    _resource_type = Profile

    @validate_args(profile_uuid=[of_type(six.text_type)])
    def get(self, profile_uuid):
        return self.client.request(
            'GET', ('Profile', profile_uuid), response_type=None)

    def list(self):
        return self.client.request(
            'GET', ('Profile'),
            to_param_dict(self.list, locals()),
            response_type=None,
            objects_type=None)

    @validate_args(profile_uuid=[of_type(six.text_type)])
    def delete(self, profile_uuid):
        return self.client.request(
            'DELETE', ('Profile', profile_uuid),
            to_param_dict(self.list, locals()),
            response_type=None,
            objects_type=None)
    
    @validate_args(
        originator=[optional(of_type(six.text_type))],
        profile_alias=[optional(of_type(six.text_type))],
        customer_type=[optional(of_type(six.text_type))],
        entity_type=[optional(of_type(six.text_type))],
        company_name=[optional(of_type(six.text_type))],
        ein=[optional(of_type(six.text_type))],
        ein_issuing_country=[optional(of_type(six.text_type))],
        stock_symbol=[optional(of_type(six.text_type))],
        stock_exchange=[optional(of_type(six.text_type))],
        website=[optional(of_type(six.text_type))],
        vertical=[optional(of_type(six.text_type))],
        alt_business_id=[optional(of_type(six.text_type))],
        alt_business_id_type=[optional(of_type(six.text_type))],
        plivo_subaccount=[optional(of_type(six.text_type))],
        address=[optional(of_type_exact(dict))],
        authorized_contact=[optional(of_type_exact(dict))])
    def create(self,
               originator,
               profile_alias,
               customer_type,
               entity_type,
               company_name,
               ein,
               ein_issuing_country,
               stock_symbol,
               stock_exchange,
               website,
               vertical,
               alt_business_id,
               alt_business_id_type,
               plivo_subaccount,
               address={},
               authorized_contact={}):
        return self.client.request('POST', ('Profile', ),
                                   to_param_dict(self.create, locals()))