from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import Ipoteka
from .serializers import IpotekaSerializer


class IpotekaModelViewSet(viewsets.ModelViewSet):
    serializer_class = IpotekaSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['rate_min', 'rate_max', 'payment_min', 'payment_max']
    ordering_fields = ['rate_max', 'payment_max']

    def get_queryset(self) -> QuerySet[Ipoteka]:
        """
        The price must be less or equal than payment_max. Otherwise, it is wrong

        :return: QuerySet[Ipoteka]
        :except ValueError, TypeError: Returns errors if the URL parameter is specified incorrectly
        """
        qs = Ipoteka.objects.all()
        price = self.request.query_params.get('price')
        try:
            if price is not None:
                return qs.filter(payment_max__gte=price)
            return qs
        except (TypeError, ValueError):
            return qs