import uuid
from django.db import models

status_choice = (
        ('ACTIVE', 'active'),
        ('CANCELLED', 'cancelled'),
        ('PENDING', 'pending')
        )

class Offering(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=40, choices=status_choice, default='ACTIVE')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    offering = models.ForeignKey(to=Offering, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=40, choices=status_choice, default='ACTIVE')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    """
    Concrete base class for jobs.
    """
    JOB_STATUS_CHOICES = [('new', 'New'),
                          ('init', 'Init'),
                          ('requested', 'Requested'),
                          ('retrive_error', 'Retrive_Error'),
                          ('scheduled', 'Scheduled'),
                          ('pending', 'Pending'),
                          ('running', 'Running'),
                          ('succeeded', 'Succeeded'),
                          ('closed', 'Closed'),
                          ('waiting', 'Waiting'),
                          ('failed', 'Failed'),
                          ('error', 'Error'),
                          ('timeout', 'Timeout'),
                          ('canceled', 'Canceled'),
                          ('canceling', 'Canceling'),
                          ('paused', 'Paused'),
                          ('pausing', 'Pausing'),
                          ('resuming', 'Resuming')]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    workflow_name = models.TextField()
    requester = models.TextField()
    job_status = models.CharField(max_length=32, choices=JOB_STATUS_CHOICES, default='init', editable=True)
    execution_id = models.CharField(max_length=50, blank=True)
    triger_at = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on', ]
