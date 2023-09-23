from collections import namedtuple
from http import HTTPStatus

from django.urls import reverse

Page = namedtuple('Page', ['url', 'expected_codes'])

MAIN_PAGES = (
    Page(
        reverse('calc:landing'),
        {
            'guest': HTTPStatus.OK,
            'user_owner': HTTPStatus.OK,
            'user_not_owner': HTTPStatus.OK,
        }
    ),
    Page(
        reverse('calc:profile', args=('gavagaver',)),
        {
            'guest': HTTPStatus.FORBIDDEN,
            'user_owner': HTTPStatus.OK,
            'user_not_owner': HTTPStatus.FORBIDDEN,
        }
    ),
)

DETAIL_PAGES = (
    Page(
        reverse('calc:site_detail', args=('8',)),
        {
            'guest': HTTPStatus.FORBIDDEN,
            'user_owner': HTTPStatus.OK,
            'user_not_owner': HTTPStatus.FORBIDDEN,
        }
    ),
    Page(
        reverse('calc:construction_detail', args=('11',)),
        {
            'guest': HTTPStatus.FORBIDDEN,
            'user_owner': HTTPStatus.OK,
            'user_not_owner': HTTPStatus.FORBIDDEN,
        }
    ),
    Page(
        reverse('calc:folder_detail', args=('12',)),
        {
            'guest': HTTPStatus.FORBIDDEN,
            'user_owner': HTTPStatus.OK,
            'user_not_owner': HTTPStatus.FORBIDDEN,
        }
    ),
    Page(
        reverse('calc:element_detail', args=('12',)),
        {
            'guest': HTTPStatus.FORBIDDEN,
            'user_owner': HTTPStatus.OK,
            'user_not_owner': HTTPStatus.FORBIDDEN,
        }
    ),
)

PAGES_AND_EXPECTED_RESPONSE_CODES = (
    MAIN_PAGES
    + DETAIL_PAGES
)
