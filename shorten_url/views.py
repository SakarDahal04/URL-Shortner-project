from django.shortcuts import render, redirect
from rest_framework import generics
from shorten_url.models import ShortUrl
from shorten_url.serializer import ShortenUrlSerializer

from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# Create your views here.
class ShortenUrlCreateAPIView(generics.CreateAPIView):
    queryset = ShortUrl.objects.all()
    serializer_class = ShortenUrlSerializer
    
    def get_permissions(self):
        print("authenticating")
        self.permission_classes = [IsAuthenticatedOrReadOnly]

        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]

        print("Set permission")

        return super().get_permissions()
    
    def perform_create(self, serializer):
        print("Creating....")
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # This lets serializer use request.build_absolute_uri()
        return context
    
    
class ShortUrlRedirectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, short_code):
        short_url = get_object_or_404(ShortUrl, short_code=short_code)
        return redirect(short_url.original_url)

class ShortUrlListAPIView(generics.ListAPIView):
    serializer_class = ShortenUrlSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ShortUrl.objects.filter(owner=self.request.user)
    
class ShortUrlRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShortenUrlSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "short_url_id"
    
    def get_queryset(self):
        # Only return objects owned by the authenticated user
        return ShortUrl.objects.filter(owner=self.request.user)
    