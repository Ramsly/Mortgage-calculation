from typing import Any

from rest_framework import serializers

from .models import Ipoteka


class IpotekaSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Ipoteka
        fields = '__all__'

    def get_payment(self, obj) -> int:
        """
        :return: Payment value. float | int
        :rtype: float | int
        :except ValueError, TypeError: Returns errors if URL parameters were incorrectly provided
        """
        try:
            price = int(self.context.get('request').query_params.get('price', None))
            deposit = int(self.context.get('request').query_params.get('deposit', None))
            term = int(self.context.get('request').query_params.get('term', None))
            if price == 0 or term == 0:
                return 0
            return self._get_offer_result(price, deposit, term, obj)
        except (ValueError, TypeError):
            return 0

    def _get_offer_result(self, price: int, deposit: int, term: int, obj: Any) -> int:
        """
        :return: Price of offer
        :rtype: float | int
        """
        price_with_dep = (price - (price * deposit / 100))
        percent_every_m = obj.rate_min / 12 / 100
        months = term * 12
        return int(round((price_with_dep * percent_every_m) / (1 - (1 + percent_every_m) ** (1 - months)), 0))
