from rest_framework import serializers

from api.models import IPLocalization, Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class RawIPLocalizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = IPLocalization
        fields = '__all__'


class IPLocalizationSerializer(RawIPLocalizationSerializer):
    currency = CurrencySerializer(many=False, read_only=True)


class SearchDBSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(required=False)
    url = serializers.URLField(required=False)

    def _validate_at_least_one_argument_provided(self, data):
        if ('ip' in data) or ('url' in data):
            return
        raise serializers.ValidationError("At least one of ['ip', 'url'] search parameters should be specified")

    def validate(self, data):
        self._validate_at_least_one_argument_provided(data)
        return data
