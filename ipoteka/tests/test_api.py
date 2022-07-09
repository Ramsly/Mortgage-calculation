import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ipoteka.models import Ipoteka
from ipoteka.serializers import IpotekaSerializer


class IpotekaApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.offer_1 = Ipoteka.objects.create(bank_name='test',
                                              term_min=1,
                                              term_max=3,
                                              rate_min=1.5,
                                              rate_max=4.8,
                                              payment_min=12345,
                                              payment_max=123456)
        self.offer_2 = Ipoteka.objects.create(bank_name='test_1',
                                              term_min=1,
                                              term_max=3,
                                              rate_min=1.5,
                                              rate_max=4.8,
                                              payment_min=12345,
                                              payment_max=123456)   
        self.data = {
            'bank_name': 'test',
            'term_min': 1,
            'term_max': 3,
            'rate_min': 1.0,
            'rate_max': 2.5,
            'payment_min': 10000,
            'payment_max': 100000,
        }

    def test_get(self):
        url = reverse('offer-list')
        response = self.client.get(url, data={'price': 1000000, 'deposit': 10, 'term': 20})
        serializer_data = IpotekaSerializer([self.offer_1, self.offer_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        url = reverse('offer-list')
        data = {
            **self.data   
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(3, Ipoteka.objects.all().count())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('offer-detail', args=(self.offer_1.id,))
        data = {
            **self.data
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete(self):
        url = reverse('offer-detail', args=(self.offer_1.id,))
        data = {
            'bank_name': self.offer_1.bank_name,
            'term_min': self.offer_1.term_min,
            'term_max': self.offer_1.term_max,
            'rate_min': self.offer_1.rate_min,
            'rate_max': self.offer_1.rate_max,
            'payment_min': self.offer_1.payment_min,
            'payment_max': self.offer_1.payment_max,
        }
        json_data = json.dumps(data)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        self.assertEqual(1, Ipoteka.objects.all().count())
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_filter(self):
        url = reverse('offer-list')
        response_1 = self.client.get(url, data={'rate_min': 1.5})
        response_2 = self.client.get(url, data={'payment_max': 123456})
        serilizer_data = IpotekaSerializer([self.offer_1, self.offer_2], many=True).data
        self.assertEqual(serilizer_data, response_1.data['results'])
        self.assertEqual(status.HTTP_200_OK, response_1.status_code)
        self.assertEqual(serilizer_data, response_2.data['results'])
        self.assertEqual(status.HTTP_200_OK, response_2.status_code)
