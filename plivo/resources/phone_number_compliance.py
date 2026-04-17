import json
import os
from plivo.base import PlivoResource, PlivoResourceInterface


class PhoneNumberComplianceRequirement(PlivoResource):
    _name = 'PhoneNumberComplianceRequirement'
    _identifier_string = 'requirement_id'


class PhoneNumberComplianceRequirements(PlivoResourceInterface):
    _resource_type = PhoneNumberComplianceRequirement

    def get(self, country_iso=None, number_type=None, user_type=None):
        # GET /PhoneNumber/Compliance/Requirements
        params = {}
        if country_iso:
            params['country_iso'] = country_iso
        if number_type:
            params['number_type'] = number_type
        if user_type:
            params['user_type'] = user_type
        return self.client.request(
            'GET',
            ('PhoneNumber', 'Compliance', 'Requirements'),
            params
        )


class PhoneNumberCompliance(PlivoResource):
    _name = 'PhoneNumberCompliance'
    _identifier_string = 'compliance_id'


class PhoneNumberComplianceApplications(PlivoResourceInterface):
    _resource_type = PhoneNumberCompliance

    def create(self, data=None, documents=None):
        """
        data: dict with keys country_iso, number_type, alias, end_user, documents, callback_url, callback_method
        documents: list of local file paths for document uploads
        """
        payload, files = _build_compliance_multipart(data, documents)
        return self.client.request(
            'POST',
            ('PhoneNumber', 'Compliance'),
            payload,
            files=files
        )

    def list(self, limit=None, offset=None, status=None, country_iso=None,
             number_type=None, user_type=None, alias=None, expand=None):
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if status:
            params['status'] = status
        if country_iso:
            params['country_iso'] = country_iso
        if number_type:
            params['number_type'] = number_type
        if user_type:
            params['user_type'] = user_type
        if alias:
            params['alias'] = alias
        if expand:
            params['expand'] = expand
        return self.client.request(
            'GET',
            ('PhoneNumber', 'Compliance'),
            params
        )

    def get(self, compliance_id, expand=None):
        params = {}
        if expand:
            params['expand'] = expand
        return self.client.request(
            'GET',
            ('PhoneNumber', 'Compliance', compliance_id),
            params
        )

    def update(self, compliance_id, data=None, documents=None):
        payload, files = _build_compliance_multipart(data, documents)
        return self.client.request(
            'PATCH',
            ('PhoneNumber', 'Compliance', compliance_id),
            payload,
            files=files
        )

    def delete(self, compliance_id):
        return self.client.request(
            'DELETE',
            ('PhoneNumber', 'Compliance', compliance_id)
        )


class PhoneNumberComplianceLink(PlivoResourceInterface):

    def link(self, numbers=None):
        """
        numbers: list of dicts, each with 'number' and 'compliance_application_id'
        """
        return self.client.request(
            'POST',
            ('PhoneNumber', 'Compliance', 'Link'),
            dict(numbers=numbers)
        )


def _build_compliance_multipart(data, documents):
    payload = {}
    files = {}
    if data:
        payload['data'] = json.dumps(data)
    if documents:
        for idx, doc_path in enumerate(documents):
            field_name = 'documents[{}].file'.format(idx)
            files[field_name] = (os.path.basename(doc_path), open(doc_path, 'rb'))
    return payload, files
