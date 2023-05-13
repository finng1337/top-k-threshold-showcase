from processor.models import Processor, RealProcessor
import csv

def run():
    RealProcessor.objects.all().delete()
    Processor.objects.all().delete()

    with open('datasets/amd.csv') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            processor = RealProcessor(
                name=row[0],
                cores=row[1],
                cores_normalized=row[2],
                threads=row[3],
                threads_normalized=row[4],
                frequency=row[5],
                frequency_normalized=row[6],
                boost_frequency=row[7],
                boost_frequency_normalized=row[8],
                cache=row[9],
                cache_normalized=row[10],
                lithography=row[11],
                lithography_normalized=row[12],
                tdp=row[13],
                tdp_normalized=row[14],
            )
            processor.save()
    print('Real processors imported')

    print('Importing generated processors')
    with open('datasets/experiment.csv') as file:
        i = 0
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if i % 1000 == 0:
                print('Imported: ' + str(i))
            i += 1
            processor = Processor(
                cores_normalized=row[0],
                threads_normalized=row[1],
                frequency_normalized=row[2],
                boost_frequency_normalized=row[3],
                cache_normalized=row[4],
                lithography_normalized=row[5],
                tdp_normalized=row[6],
            )
            processor.save()
    print('Generated processors imported')