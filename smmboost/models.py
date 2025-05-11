from django.db import models

class Service(models.Model):
    service_id = models.IntegerField()
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    rate = models.FloatField()
    min_quantity = models.IntegerField()
    max_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.category}"


class Order(models.Model):
    api_order_id = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    link = models.URLField()
    quantity = models.IntegerField()
    charge = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    start_count = models.IntegerField(null=True, blank=True)
    remains = models.IntegerField(null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.api_order_id} - {self.status}"
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'