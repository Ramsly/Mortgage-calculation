from multiprocessing import context
from urllib import request
from django.test import TestCase, RequestFactory
from django.urls import reverse

from ipoteka.models import Ipoteka
from ipoteka.serializers import IpotekaSerializer
from ipoteka.views import IpotekaModelViewSet


class SerializerTestCase(TestCase):
    def test_ser(self):
        url = reverse('offer-list')
        view = IpotekaModelViewSet.as_view({'get': 'list'})
        request = RequestFactory()
        request = request.get(url, data={'price': 10000000, 'deposit': 10, 'term': 20})
        offer_1 = Ipoteka.objects.create(bank_name='test',
                                         term_min=1,
                                         term_max=3,
                                         rate_min=1.0,
                                         rate_max=2.5,
                                         payment_min=10000,
                                         payment_max=100000)
        offer_2 = Ipoteka.objects.create(bank_name='test123',
                                         term_min=2,
                                         term_max=4,
                                         rate_min=1.4,
                                         rate_max=2.5,
                                         payment_min=15000,
                                         payment_max=150000)
        expected_data = [
            {
                'id': offer_1.id,
                'bank_name': 'test',
                'term_min': 1,
                'term_max': 3,
                'rate_min': 1.0,
                'rate_max': 2.5,
                'payment_min': 10000,
                'payment_max': 100000,
            },
            {
                'id': offer_2.id,
                'bank_name': 'test123',
                'term_min': 2,
                'term_max': 4,
                'rate_min': 1.4,
                'rate_max': 2.5,
                'payment_min': 15000,
                'payment_max': 150000,
            }
        ]
        data = IpotekaSerializer([offer_1, offer_2], context={'request': view(request)}, many=True).data
        self.assertEqual(data, expected_data)