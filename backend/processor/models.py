from django.db import models

class Processor(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=128, default='')
    cores = models.IntegerField(blank=True, null=True)
    cores_normalized = models.FloatField()
    threads = models.IntegerField(blank=True, null=True)
    threads_normalized = models.FloatField()
    frequency = models.IntegerField(blank=True, null=True)
    frequency_normalized = models.FloatField()
    boost_frequency = models.IntegerField(blank=True, null=True)
    boost_frequency_normalized = models.FloatField()
    cache = models.IntegerField(blank=True, null=True)
    cache_normalized = models.FloatField()
    lithography = models.IntegerField(blank=True, null=True)
    lithography_normalized = models.FloatField()
    tdp = models.IntegerField(blank=True, null=True)
    tdp_normalized = models.FloatField()

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name