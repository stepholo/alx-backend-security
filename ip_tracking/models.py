from django.db import models


# Create your models here.
class RequestLog(models.Model):
    """Model to log requests with IP addresses and user agents."""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']


class BlockedIP(models.Model):
    """Model to store blocked IP addresses."""
    ip_address = models.GenericIPAddressField(unique=True)
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blocked IP: {self.ip_address} at {self.blocked_at}"

    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"
        ordering = ['-blocked_at']


class SuspiciousIP(models.Model):
    """Model to store suspicious IP addresses."""
    ip_address = models.GenericIPAddressField(unique=True)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suspicious IP: {self.ip_address} at {self.detected_at}"

    class Meta:
        verbose_name = "Suspicious IP"
        verbose_name_plural = "Suspicious IPs"
        ordering = ['-detected_at']