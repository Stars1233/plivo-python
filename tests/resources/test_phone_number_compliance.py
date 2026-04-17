# -*- coding: utf-8 -*-

from plivo import exceptions
from tests.base import PlivoResourceTestCase


class PhoneNumberComplianceRequirementsTest(PlivoResourceTestCase):

    def test_get_requirements(self):
        expected_response = {
            'requirement_id': 'req_123',
            'country_iso': 'DE',
            'number_type': 'local',
            'user_type': 'business',
            'document_types': [
                {
                    'document_type': 'national_id',
                    'description': 'National ID Card'
                },
                {
                    'document_type': 'utility_bill',
                    'description': 'Utility Bill'
                }
            ]
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance_requirements.get(
            country_iso='DE', number_type='local', user_type='business')

        self.assertEqual(
            self.client.current_request.url,
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/PhoneNumber/Compliance/Requirements/?country_iso=DE&number_type=local&user_type=business')
        self.assertEqual(self.client.current_request.method, 'GET')
        self.assertEqual(response.requirement_id, expected_response['requirement_id'])

    def test_get_requirements_url_path(self):
        expected_response = {
            'requirement_id': 'req_456',
            'document_types': []
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        self.client.phone_number_compliance_requirements.get(
            country_iso='US')

        # Verify the URL contains the correct path segments
        self.assertIn(
            '/PhoneNumber/Compliance/Requirements/',
            self.client.current_request.url)
        self.assertEqual(self.client.current_request.method, 'GET')

    def test_get_requirements_empty_document_types(self):
        expected_response = {
            'requirement_id': 'req_789',
            'country_iso': 'US',
            'number_type': 'local',
            'document_types': []
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance_requirements.get(
            country_iso='US', number_type='local')

        self.assertEqual(self.client.current_request.method, 'GET')
        self.assertEqual(len(response.document_types), 0)

    def test_get_requirements_partial_args_no_none_in_url(self):
        """Calling get() with only country_iso should not send
        number_type=None or user_type=None in the query string."""
        expected_response = {
            'requirement_id': 'req_partial',
            'document_types': []
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        self.client.phone_number_compliance_requirements.get(
            country_iso='IN')

        url = self.client.current_request.url
        self.assertIn('country_iso=IN', url)
        self.assertNotIn('None', url)
        self.assertNotIn('number_type', url)
        self.assertNotIn('user_type', url)
        self.assertEqual(self.client.current_request.method, 'GET')

    def test_get_requirements_no_args_no_none_in_url(self):
        """Calling get() with no arguments should produce a clean URL
        with no query parameters containing None."""
        expected_response = {
            'requirement_id': 'req_noargs',
            'document_types': []
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        self.client.phone_number_compliance_requirements.get()

        url = self.client.current_request.url
        self.assertNotIn('None', url)
        self.assertNotIn('number_type', url)
        self.assertNotIn('user_type', url)
        self.assertNotIn('country_iso', url)
        self.assertEqual(self.client.current_request.method, 'GET')


class PhoneNumberComplianceApplicationsTest(PlivoResourceTestCase):

    def test_create(self):
        expected_response = {
            'compliance_id': 'comp_abc123',
            'message': 'Compliance application created successfully'
        }
        self.client.set_expected_response(
            status_code=201, data_to_return=expected_response)

        response = self.client.phone_number_compliance.create(
            data={
                'country_iso': 'DE',
                'number_type': 'local',
                'alias': 'My German Number',
                'end_user': {'name': 'Test User'},
            })

        self.assertIn(
            '/PhoneNumber/Compliance/',
            self.client.current_request.url)
        self.assertEqual(self.client.current_request.method, 'POST')
        self.assertEqual(response.compliance_id, expected_response['compliance_id'])
        self.assertEqual(response.message, expected_response['message'])

    def test_create_multipart_data_structure(self):
        expected_response = {
            'compliance_id': 'comp_def456',
            'message': 'created'
        }
        self.client.set_expected_response(
            status_code=201, data_to_return=expected_response)

        data = {
            'country_iso': 'GB',
            'number_type': 'mobile',
            'alias': 'UK Mobile',
            'end_user': {'name': 'Jane Doe'},
            'callback_url': 'https://example.com/callback',
            'callback_method': 'POST',
        }
        response = self.client.phone_number_compliance.create(data=data)

        self.assertEqual(self.client.current_request.method, 'POST')
        self.assertEqual(response.compliance_id, 'comp_def456')

    def test_create_without_documents(self):
        """Create without documents parameter should succeed and use
        multipart/form-data (not application/json)."""
        expected_response = {
            'compliance_id': 'comp_nodoc',
            'message': 'created'
        }
        self.client.set_expected_response(
            status_code=201, data_to_return=expected_response)

        response = self.client.phone_number_compliance.create(
            data={
                'country_iso': 'IN',
                'number_type': 'local',
                'alias': 'India Local',
                'end_user': {'name': 'Test User'},
            })

        self.assertEqual(self.client.current_request.method, 'POST')
        self.assertEqual(response.compliance_id, 'comp_nodoc')
        # Verify the request uses multipart encoding, not JSON
        content_type = self.client.current_request.headers['Content-Type']
        self.assertTrue(
            any([
                'multipart' in content_type,
                'www-form-urlencoded' in content_type
            ]))

    def test_create_with_documents_none(self):
        """Create with documents=None should succeed and use
        multipart/form-data."""
        expected_response = {
            'compliance_id': 'comp_docnone',
            'message': 'created'
        }
        self.client.set_expected_response(
            status_code=201, data_to_return=expected_response)

        response = self.client.phone_number_compliance.create(
            data={
                'country_iso': 'GB',
                'number_type': 'mobile',
                'alias': 'UK Mobile',
                'end_user': {'name': 'Jane Doe'},
            },
            documents=None)

        self.assertEqual(self.client.current_request.method, 'POST')
        self.assertEqual(response.compliance_id, 'comp_docnone')
        content_type = self.client.current_request.headers['Content-Type']
        self.assertTrue(
            any([
                'multipart' in content_type,
                'www-form-urlencoded' in content_type
            ]))

    def test_update_without_documents(self):
        """Update without documents should succeed and use
        multipart/form-data."""
        expected_response = {
            'message': 'updated',
            'compliance': {
                'compliance_id': 'comp_upd_nodoc',
                'status': 'pending'
            }
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.update(
            'comp_upd_nodoc',
            data={'alias': 'New Alias'})

        self.assertEqual(self.client.current_request.method, 'PATCH')
        self.assertEqual(response.message, 'updated')
        content_type = self.client.current_request.headers['Content-Type']
        self.assertTrue(
            any([
                'multipart' in content_type,
                'www-form-urlencoded' in content_type
            ]))

    def test_list(self):
        expected_response = {
            'meta': {
                'limit': 20,
                'offset': 0,
                'next': '/v1/Account/MAXXXXXXXXXXXXXXXXXX/PhoneNumber/Compliance/?limit=20&offset=20',
                'previous': None,
                'total_count': 2
            },
            'compliances': [
                {
                    'compliance_id': 'comp_001',
                    'status': 'approved',
                    'country_iso': 'DE',
                    'alias': 'German Line'
                },
                {
                    'compliance_id': 'comp_002',
                    'status': 'pending',
                    'country_iso': 'GB',
                    'alias': 'UK Line'
                }
            ]
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.list()

        self.assertIn(
            '/PhoneNumber/Compliance/',
            self.client.current_request.url)
        self.assertEqual(self.client.current_request.method, 'GET')
        self.assertEqual(len(response.compliances), 2)

    def test_list_with_filters(self):
        expected_response = {
            'meta': {
                'limit': 10,
                'offset': 0,
                'next': None,
                'previous': None,
                'total_count': 1
            },
            'compliances': [
                {
                    'compliance_id': 'comp_001',
                    'status': 'approved',
                    'country_iso': 'DE'
                }
            ]
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.list(
            status='approved', country_iso='DE', limit=10, offset=0)

        url = self.client.current_request.url
        self.assertIn('status=approved', url)
        self.assertIn('country_iso=DE', url)
        self.assertIn('limit=10', url)
        self.assertIn('offset=0', url)
        self.assertEqual(self.client.current_request.method, 'GET')

    def test_list_empty(self):
        expected_response = {
            'meta': {
                'limit': 20,
                'offset': 0,
                'next': None,
                'previous': None,
                'total_count': 0
            },
            'compliances': []
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.list()

        self.assertEqual(self.client.current_request.method, 'GET')
        self.assertEqual(len(response.compliances), 0)
        self.assertEqual(response.meta.total_count, 0)

    def test_get(self):
        expected_response = {
            'compliance': {
                'compliance_id': 'comp_abc123',
                'status': 'approved',
                'country_iso': 'DE',
                'number_type': 'local',
                'alias': 'My German Number',
                'end_user': {
                    'name': 'Test User',
                    'email': 'test@example.com'
                },
                'documents': [
                    {'document_id': 'doc_001', 'document_type': 'national_id'}
                ],
                'created_at': '2025-01-15T10:00:00Z',
                'updated_at': '2025-01-16T12:00:00Z'
            }
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.get('comp_abc123')

        self.assertEqual(
            self.client.current_request.url,
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/PhoneNumber/Compliance/comp_abc123/')
        self.assertEqual(self.client.current_request.method, 'GET')
        self.assertEqual(response.compliance.compliance_id, 'comp_abc123')

    def test_get_with_expand(self):
        expected_response = {
            'compliance': {
                'compliance_id': 'comp_abc123',
                'status': 'approved',
                'country_iso': 'DE',
                'end_user': {'name': 'Test User'},
                'documents': []
            }
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.get(
            'comp_abc123', expand='end_user,documents')

        self.assertIn('expand=end_user%2Cdocuments', self.client.current_request.url)
        self.assertEqual(self.client.current_request.method, 'GET')

    def test_get_response_fields(self):
        expected_response = {
            'compliance': {
                'compliance_id': 'comp_full',
                'status': 'pending',
                'country_iso': 'FR',
                'number_type': 'mobile',
                'user_type': 'business',
                'alias': 'French Mobile',
                'end_user': {
                    'name': 'Acme Corp',
                    'email': 'admin@acme.com',
                    'phone': '+33123456789'
                },
                'documents': [
                    {
                        'document_id': 'doc_100',
                        'document_type': 'national_id',
                        'status': 'verified'
                    },
                    {
                        'document_id': 'doc_101',
                        'document_type': 'utility_bill',
                        'status': 'pending'
                    }
                ],
                'callback_url': 'https://example.com/callback',
                'callback_method': 'POST',
                'created_at': '2025-06-01T08:00:00Z',
                'updated_at': '2025-06-02T09:30:00Z'
            }
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.get('comp_full')

        compliance = response.compliance
        self.assertEqual(compliance.compliance_id, 'comp_full')
        self.assertEqual(compliance.status, 'pending')
        self.assertEqual(compliance.country_iso, 'FR')
        self.assertEqual(compliance.number_type, 'mobile')
        self.assertEqual(compliance.alias, 'French Mobile')
        self.assertEqual(compliance.end_user.name, 'Acme Corp')
        self.assertEqual(len(compliance.documents), 2)

    def test_get_not_found(self):
        expected_response = {
            'error': 'Compliance application not found'
        }
        self.client.set_expected_response(
            status_code=404, data_to_return=expected_response)

        self.assertRaises(
            exceptions.ResourceNotFoundError,
            self.client.phone_number_compliance.get,
            'comp_nonexistent')

    def test_update(self):
        expected_response = {
            'message': 'Compliance application updated successfully',
            'compliance': {
                'compliance_id': 'comp_abc123',
                'status': 'pending',
                'alias': 'Updated Alias'
            }
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.update(
            'comp_abc123',
            data={'alias': 'Updated Alias'})

        self.assertIn(
            '/PhoneNumber/Compliance/comp_abc123/',
            self.client.current_request.url)
        self.assertEqual(self.client.current_request.method, 'PATCH')
        self.assertEqual(response.message, 'Compliance application updated successfully')

    def test_update_http_method(self):
        expected_response = {
            'message': 'updated',
            'compliance': {
                'compliance_id': 'comp_xyz789',
                'status': 'pending'
            }
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        self.client.phone_number_compliance.update(
            'comp_xyz789',
            data={'end_user': {'name': 'New Name'}})

        # Verify PATCH method is used (not POST or PUT)
        self.assertEqual(self.client.current_request.method, 'PATCH')

    def test_delete(self):
        expected_response = {
            'compliance_id': 'comp_abc123',
            'message': 'Compliance application deleted successfully'
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.delete('comp_abc123')

        self.assertIn(
            '/PhoneNumber/Compliance/comp_abc123/',
            self.client.current_request.url)
        self.assertEqual(self.client.current_request.method, 'DELETE')
        self.assertEqual(response.compliance_id, 'comp_abc123')
        self.assertEqual(response.message, 'Compliance application deleted successfully')

    def test_delete_not_found(self):
        expected_response = {
            'error': 'Compliance application not found'
        }
        self.client.set_expected_response(
            status_code=404, data_to_return=expected_response)

        self.assertRaises(
            exceptions.ResourceNotFoundError,
            self.client.phone_number_compliance.delete,
            'comp_nonexistent')

    def test_list_pagination_meta(self):
        expected_response = {
            'meta': {
                'limit': 5,
                'offset': 10,
                'next': '/v1/Account/MAXXXXXXXXXXXXXXXXXX/PhoneNumber/Compliance/?limit=5&offset=15',
                'previous': '/v1/Account/MAXXXXXXXXXXXXXXXXXX/PhoneNumber/Compliance/?limit=5&offset=5',
                'total_count': 25
            },
            'compliances': [
                {'compliance_id': 'comp_010', 'status': 'approved'},
                {'compliance_id': 'comp_011', 'status': 'pending'},
                {'compliance_id': 'comp_012', 'status': 'approved'},
                {'compliance_id': 'comp_013', 'status': 'rejected'},
                {'compliance_id': 'comp_014', 'status': 'pending'}
            ]
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance.list(limit=5, offset=10)

        self.assertEqual(response.meta.limit, 5)
        self.assertEqual(response.meta.offset, 10)
        self.assertEqual(response.meta.total_count, 25)
        self.assertIsNotNone(response.meta.next)
        self.assertIsNotNone(response.meta.previous)
        self.assertEqual(len(response.compliances), 5)


class PhoneNumberComplianceLinkTest(PlivoResourceTestCase):

    def test_link(self):
        expected_response = {
            'report': [
                {
                    'number': '+4930123456',
                    'compliance_application_id': 'comp_abc123',
                    'status': 'success',
                    'message': 'Number linked successfully'
                },
                {
                    'number': '+4930654321',
                    'compliance_application_id': 'comp_abc123',
                    'status': 'success',
                    'message': 'Number linked successfully'
                }
            ]
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance_link.link(
            numbers=[
                {'number': '+4930123456', 'compliance_application_id': 'comp_abc123'},
                {'number': '+4930654321', 'compliance_application_id': 'comp_abc123'}
            ])

        self.assertIn(
            '/PhoneNumber/Compliance/Link/',
            self.client.current_request.url)
        self.assertEqual(self.client.current_request.method, 'POST')
        self.assertEqual(len(response.report), 2)

    def test_link_empty_report(self):
        expected_response = {
            'report': []
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        response = self.client.phone_number_compliance_link.link(numbers=[])

        self.assertEqual(self.client.current_request.method, 'POST')
        self.assertEqual(len(response.report), 0)

    def test_link_request_body(self):
        expected_response = {
            'report': [
                {
                    'number': '+441234567890',
                    'compliance_application_id': 'comp_uk001',
                    'status': 'success'
                }
            ]
        }
        self.client.set_expected_response(
            status_code=200, data_to_return=expected_response)

        numbers = [
            {'number': '+441234567890', 'compliance_application_id': 'comp_uk001'}
        ]
        response = self.client.phone_number_compliance_link.link(numbers=numbers)

        self.assertEqual(
            self.client.current_request.url,
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/PhoneNumber/Compliance/Link/')
        self.assertEqual(self.client.current_request.method, 'POST')
        self.assertEqual(len(response.report), 1)
        self.assertEqual(response.report[0].number, '+441234567890')
