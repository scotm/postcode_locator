__author__ = 'scotm'
# Converts postcode.csv files available from the following address:
# http://www.ordnancesurvey.co.uk/business-and-government/products/code-point-open.html
import time
import csv
from itertools import imap
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from postcode_locator.models import PostcodeMapping

from core.utilities.constants import postcodeareas
from core.utilities.functions import chunked

postcodes_already = set(PostcodeMapping.objects.all().values_list('postcode',flat=True))

def process_postcode_data(line):
    return PostcodeMapping(postcode=line['postcode'],
                           point=Point(float(line['longitude']), float(line['latitude'])))


def fill_up_db(postcode_filename, chunk_size=500):
    i = 0
    with open(postcode_filename) as myfile:
        # Read in the postcodes file - and remove duplicates
        print "Reading in postcode file"
        reader = (i for i in csv.DictReader(myfile) if i['postcode'][:2] in postcodeareas)
        reader = (x for x in reader if x['postcode'] not in postcodes_already)
        chunker = chunked(imap(process_postcode_data, reader), chunk_size)
        failed_chunks = []
        for chunk in chunker:
            try:
                PostcodeMapping.objects.bulk_create(chunk)
            except KeyboardInterrupt:
                raise
            except:
                failed_chunks += chunk
                print "Chunk failed. Will retry at the end."
                continue
            i += len(chunk)

    if failed_chunks:
        print "Applying %d failed chunks individually" % (len(failed_chunks))
    for i in failed_chunks:
        try:
            print "Trying %s" % i.postcode
            i.save()
        except:
            print "%s failed" % unicode(i)


class Command(BaseCommand):
    help = 'Fills up the DB with postcode points'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=unicode)

    def handle(self, *args, **options):
        print options, args
        filename = args[0]
        fill_up_db(filename)