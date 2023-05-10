from django.db import models

class Processor(models.Model):
    cores_normalized = models.FloatField()
    threads_normalized = models.FloatField()
    frequency_normalized = models.FloatField()
    boost_frequency_normalized = models.FloatField()
    cache_normalized = models.FloatField()
    lithography_normalized = models.FloatField()
    tdp_normalized = models.FloatField()

    def __str__(self):
        return self.pk

    def __lt__(self, other):
        return self.pk < other.pk

    def __gt__(self, other):
        return self.pk > other.pk

class RealProcessor(Processor):
    name = models.CharField(max_length=128, default='')
    cores = models.IntegerField()
    threads = models.IntegerField()
    frequency = models.IntegerField()
    boost_frequency = models.IntegerField()
    cache = models.IntegerField()
    lithography = models.IntegerField()
    tdp = models.IntegerField()