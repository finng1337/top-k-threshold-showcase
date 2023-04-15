from django.db import models

class Processor(models.Model):
    name = models.CharField(max_length=64)
    cores = models.IntegerField()
    cores_normalized = models.FloatField()
    threads = models.IntegerField()
    threads_normalized = models.FloatField()
    frequency = models.IntegerField()
    frequency_normalized = models.FloatField()
    boost_frequency = models.IntegerField()
    boost_frequency_normalized = models.FloatField()
    cache = models.IntegerField()
    cache_normalized = models.FloatField()
    lithography = models.IntegerField()
    lithography_normalized = models.FloatField()
    tdp = models.IntegerField()
    tdp_normalized = models.FloatField()

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name