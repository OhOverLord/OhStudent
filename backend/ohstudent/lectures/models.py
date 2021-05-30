from django.db import models
from django.urls import reverse

from account.models import User

STATUS = [
    ('private', 'private'),
    ('public', 'public')
]

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS, default='private', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='lectures', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('lectures:lecture-detail', args=[str(self.id)])

    class Meta:
        ordering = ["-created_at"]
    
