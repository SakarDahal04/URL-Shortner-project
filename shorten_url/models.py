from django.db import models
from account.models import User

import random
import string

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class ShortUrl(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, default=generate_short_code)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="short_urls")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.short_code} of {self.owner.name}"