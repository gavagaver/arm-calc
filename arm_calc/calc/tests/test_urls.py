from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from calc.tests.pages import PAGES_AND_EXPECTED_RESPONSE_CODES

User = get_user_model()


class CalcURLsTests(TestCase):
    fixtures = ('testdata.json',)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        cache.clear()
        user_owner = User.objects.get(username='gavagaver')
        user_not_owner = User.objects.get(username='tester')
        self.guest_client = Client()
        self.authorized_client_owner = Client()
        self.authorized_client_owner.force_login(user_owner)
        self.authorized_client_not_owner = Client()
        self.authorized_client_not_owner.force_login(user_not_owner)

    def test_urls_expected_codes(self):
        """
        The pages return the expected response codes
        for the guest, user and owner.
        """
        clients = {
            'guest': self.guest_client,
            'user_owner': self.authorized_client_owner,
            'user_not_owner': self.authorized_client_not_owner,
        }

        for page in PAGES_AND_EXPECTED_RESPONSE_CODES:
            url = page.url
            expected_codes = page.expected_codes

            for name, client in clients.items():
                expected_code = expected_codes[name]

                with self.subTest(url=url):
                    response = client.get(url)

                    self.assertEqual(
                        response.status_code,
                        expected_code,
                        (
                            f'Страница "{url}" при посещении "{name}" вернула '
                            f'код ответа, отличный от ожидаемого.'
                        ),
                    )
