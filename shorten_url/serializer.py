from rest_framework import serializers
from shorten_url.models import ShortUrl


class ShortenUrlSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = ShortUrl
        fields = ("id", "owner", "original_url", "short_code", "short_url")
        read_only_fields = ["id", "owner", "short_code", "short_url"]

    def get_short_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(f'/{obj.short_code}/') if req else f'/{obj.short_code}/'