from django.db import models
from django.contrib.auth.models import User 

class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    refill_due_date = models.DateField(null=True, blank=True)
    taken = models.BooleanField(default=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

class MedicationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    taken = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user', 'medication', 'date')