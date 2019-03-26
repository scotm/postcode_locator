from __future__ import print_function

__author__ = 'scotm'
# Converts postcode.csv files available from the following address:
# http://www.ordnancesurvey.co.uk/business-and-government/products/code-point-open.html
import csv
try:
    from itertools import imap, izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest
    imap=map
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from postcode_locator.models import PostcodeMapping
from postcode_locator.constants import postcodeareas

postcodes_already = set(PostcodeMapping.objects.all().values_list('postcode', flat=True))


def chunked(iterable, n):
    _marker = object()
    for group in (list(g) for g in izip_longest(*[iter(iterable)] * n, fillvalue=_marker)):
        if group[-1] is _marker:
            # If this is the last group, remove the padding:
            del group[group.index(_marker):]
        yield group


def process_postcode_data(line):
    line['postcode'] = line['postcode'].replace(" ","")
    if 'longitude' in line and 'latitude' in line:
        return PostcodeMapping(postcode=line['postcode'], point=Point(float(line['longitude']), float(line['latitude'])))
    if 'Eastings' in line and 'Northings' in line:
        pnt = Point(float(line['Eastings']), float(line['Northings']), srid=27700)
        pnt.transform(4326)
        return PostcodeMapping(postcode=line['postcode'], point=pnt)


def fill_up_db(postcode_filename, chunk_size=5):
    i = 0
    with open(postcode_filename) as myfile:
        # Read in the postcodes file - and remove duplicates
        print("Reading in postcode file")
        reader = (i for i in csv.DictReader(myfile) if i['postcode'][:2] in postcodeareas)
        reader = (x for x in reader if x['postcode'].replace(" ","") not in postcodes_already)
        chunker = chunked(imap(process_postcode_data, reader), chunk_size)
        failed_chunks = []
        for chunk in chunker:
            print(chunk)
            try:
                PostcodeMapping.objects.bulk_create(chunk)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                failed_chunks += chunk
                print("Chunk failed. Will retry at the end.")
                continue
            i += len(chunk)

    if failed_chunks:
        print("Applying %d failed chunks individually" % (len(failed_chunks)))
    for i in failed_chunks:
        try:
            print("Trying %s" % i.postcode)
            i.save()
        except:
            print("%s failed" % i)


class Command(BaseCommand):
    help = 'Fills up the DB with postcode points'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1)

    def handle(self, *args, **options):
        try:
            filename = args[0]
        except IndexError:
            filename = options['filename'][0]
        fill_up_db(filename)