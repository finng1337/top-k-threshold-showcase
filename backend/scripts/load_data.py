from processor.models import Processor
from decimal import Decimal
import csv

def run():
    with open('datasets/amd.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Processor.objects.all().delete()

        for row in reader:
            processor = Processor(
                name=row[0],
                cores=row[1],
                cores_normalized=Decimal(row[2].replace(',', '.')),
                threads=row[3],
                threads_normalized=Decimal(row[4].replace(',', '.')),
                frequency=row[5],
                frequency_normalized=Decimal(row[6].replace(',', '.')),
                boost_frequency=row[7],
                boost_frequency_normalized=Decimal(row[8].replace(',', '.')),
                cache=row[9],
                cache_normalized=Decimal(row[10].replace(',', '.')),
                lithography=row[11],
                lithography_normalized=Decimal(row[12].replace(',', '.')),
                tdp=row[13],
                tdp_normalized=Decimal(row[14].replace(',', '.')),
            )
            processor.save()