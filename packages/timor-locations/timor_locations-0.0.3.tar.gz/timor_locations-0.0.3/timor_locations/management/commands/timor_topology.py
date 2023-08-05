
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Commands necessary to build timor 'topology' layer in postgis"


    def handle(self, *args, **options):


        topology_schema_name = "topo"
        precision = 1e-6
        tolerance = 0
        srid=4326

        self.stdout.write(self.style.SUCCESS("Creating topology"))
        with connection.cursor() as c:
            # c.execute(f"SELECT topology.DropTopology('{topology_schema_name}')")
            c.execute(f"SELECT topology.CreateTopology('{topology_schema_name}', {srid}, {precision});")
            # Add topology from the 'suco' table
            c.execute(f"SELECT topology.ST_CreateTopoGeo('{topology_schema_name}', geom) FROM timor_locations_suco;")

