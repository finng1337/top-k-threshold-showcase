from processor.models import Processor
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
                cores_normalized=row[2].replace(',', '.'),
                threads=row[3],
                threads_normalized=row[4].replace(',', '.'),
                frequency=row[5],
                frequency_normalized=row[6].replace(',', '.'),
                boost_frequency=row[7],
                boost_frequency_normalized=row[8].replace(',', '.'),
                cache=row[9],
                cache_normalized=row[10].replace(',', '.'),
                lithography=row[11],
                lithography_normalized=row[12].replace(',', '.'),
                tdp=row[13],
                tdp_normalized=row[14].replace(',', '.'),
            )
            processor.save()