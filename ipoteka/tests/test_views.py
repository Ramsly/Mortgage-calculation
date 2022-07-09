from rest_framework import status
from django.urls import reverse
from django.test import TestCase


class ViewTestCase(TestCase):

    def test_list_view(self):
        url = reverse('offer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
