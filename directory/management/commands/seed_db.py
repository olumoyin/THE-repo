import os
from django.core.management.base import BaseCommand

from directory.utils import SaveServiceLocations
from wta_api_build.settings import BASE_DIR

class Command(BaseCommand):
    help = 'Seed the database with service locations from a JSON file'

    def handle(self, *args, **kwargs):

        # Task 1: Seed the database with MTN P2P service locations
        # file_path = os.path.join('directory', 'SL_Data', 'mtn_com_geo_data.json')
        # report = SaveServiceLocations(file_path, "")
        # self.stdout.write(self.style.SUCCESS(report))

        # Task 2: Populate the database with FIAM WIFI service locations
        # file_path = os.path.join('directory', 'SL_Data', 'fiam_wifi_data.json')
        # report = SaveServiceLocations(file_path, "da7ea82a-a8eb-426f-8e2e-931995f405ae")
        # self.stdout.write(self.style.SUCCESS(report))

        # Task 3: Populate the database with LEGEND FIBER service locations
        file_path = os.path.join('directory', 'SL_Data', 'legend_metro_fiber_com_data.json')
        report = SaveServiceLocations(file_path, "319f915d-3b2f-4eb5-a572-1484a8898b17")
        self.stdout.write(self.style.SUCCESS(report))

        # Task 4: Populate the database with VODA-COM P2 service locations
        # file_path = os.path.join('directory', 'SL_Data', 'voda_com_geojson_data.json')
        # report = SaveServiceLocations(file_path, "")
        # self.stdout.write(self.style.SUCCESS(report))