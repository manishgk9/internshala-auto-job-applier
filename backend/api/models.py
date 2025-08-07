from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AppliedJobs(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('processing', 'Proccessing'),
        ('cancelled', 'Cancelled'),
    ]
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_id = models.CharField(max_length=100, unique=True,primary_key=True)
    applied_on = models.DateField(auto_now_add=True)
    url=models.CharField(max_length=400,default=None)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"{self.job_title} at {self.company_name} - {self.status}"
