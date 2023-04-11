from django.db import models

class Processor(models.Model):
    name = models.CharField(max_length=64)
    cores = models.IntegerField()
    cores_normalized = models.DecimalField(max_digits=5, decimal_places=4)
    threads = models.IntegerField()
    threads_normalized = models.DecimalField(max_digits=6, decimal_places=5)
    frequency = models.IntegerField()
    frequency_normalized = models.DecimalField(max_digits=5, decimal_places=4)
    boost_frequency = models.IntegerField()
    boost_frequency_normalized = models.DecimalField(max_digits=5, decimal_places=4)
    cache = models.IntegerField()
    cache_normalized = models.DecimalField(max_digits=8, decimal_places=7)
    lithography = models.IntegerField()
    lithography_normalized = models.DecimalField(max_digits=5, decimal_places=4)
    tdp = models.IntegerField()
    tdp_normalized = models.DecimalField(max_digits=6, decimal_places=5)

    def __str__(self):
        return self.name