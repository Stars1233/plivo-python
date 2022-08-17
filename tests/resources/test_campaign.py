from plivo import exceptions
from tests.base import PlivoResourceTestCase
from tests.decorators import with_response

class CampaignTest(PlivoResourceTestCase):
    @with_response(200)
    def test_create(self):
        sub_usecase = ["CUSTOMER_CARE","2FA"]
        response = self.client.campaign.create(brand_id = "B8OD95Z",
                campaign_alias = "campaign name sssample",
                vertical = "INSURANCE",
                usecase = "MIXED",
                sub_usecases = sub_usecase,
                description = "sample description text",
                embedded_link = False,
                embedded_phone = False,
                age_gated = False,
                direct_lending = False,
                subscriber_optin = True,
                subscriber_optout = True,
                subscriber_help = True,
                sample1 = "test 1",
                sample2 = "test 2",
                url="http://example.com/test",
                method="POST")
        self.assertEqual('POST', self.client.current_request.method)
        self.assertUrlEqual(
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/10dlc/Campaign/',
            self.client.current_request.url)

    @with_response(200)
    def test_get(self):
        response = self.client.campaign.get(campaign_id='BRPXS6E')
        # Verifying the endpoint hit
        self.assertUrlEqual(
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/10dlc/Campaign/BRPXS6E/',
            self.client.current_request.url)

        # Verifying the method used
        self.assertEqual('GET', self.client.current_request.method)

    @with_response(200)
    def test_list(self):
        res = self.client.campaign.list(limit=2, offset=0)
        # Test if ListResponseObject's __iter__ is working correctly
        self.assertGreater(len(list(res.campaigns)), 0)
        # Verifying the endpoint hit
        self.assertUrlEqual(
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/10dlc/Campaign/?limit=2&offset=0',
            self.client.current_request.url)
        # Verifying the method used
        self.assertEqual('GET', self.client.current_request.method)

    @with_response(200)
    def test_number_link(self):
        number = ['87654545465', '876650988']
        response = self.client.campaign.number_link(campaign_id='BRPXS6E',
                    url='http://example.com/test',
                    method='POST',
                    numbers=number
                    )
        self.assertEqual('POST', self.client.current_request.method)
        self.assertUrlEqual(
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/10dlc/Campaign/BRPXS6E/Number/',
            self.client.current_request.url)


    @with_response(200)
    def test_get_numbers(self):
        response = self.client.campaign.get_numbers(campaign_id='BRPXS6E',
                    limit=20, 
                    offset=0)
        self.assertEqual('GET', self.client.current_request.method)
        self.assertUrlEqual(
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/10dlc/Campaign/BRPXS6E/Number/?limit=20',
            self.client.current_request.url)

    @with_response(200)
    def test_get_number(self):
        response = self.client.campaign.get_number(campaign_id='BRPXS6E',
                                                    number='9873636363')
        self.assertEqual('GET', self.client.current_request.method)
        self.assertUrlEqual(
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/10dlc/Campaign/BRPXS6E/Number/9873636363/',
            self.client.current_request.url)

    @with_response(200)
    def test_number_unlink(self):
        response = self.client.campaign.number_unlink(campaign_id='BRPXS6E',
                                                        number='9873636363')
        self.assertEqual('DELETE', self.client.current_request.method)
        self.assertUrlEqual(
            'https://api.plivo.com/v1/Account/MAXXXXXXXXXXXXXXXXXX/10dlc/Campaign/BRPXS6E/Number/9873636363/',
            self.client.current_request.url)

