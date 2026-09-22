from django.db import models
from django.conf import settings

class SupportTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='OPEN') # OPEN, RESOLVED, CLOSED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support Ticket #{self.id} - {self.subject}"
