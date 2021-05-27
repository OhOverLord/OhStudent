from django.db import models

STATUS = [
    ('private', 'private'),
    ('public', 'public')
]

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS, default='private', blank=True)
