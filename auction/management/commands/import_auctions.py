import json
from django.core.management.base import BaseCommand
from auction.models import Auction
from shoes.models import Shoe
from datetime import datetime

class Command(BaseCommand):
    help = 'Import auctions from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        with open(json_file_path, 'r') as file:
            auctions_data = json.load(file)

        for auction_data in auctions_data:
            shoe_id = auction_data['shoe_id']
            shoe = Shoe.objects.get(id=shoe_id)

            auction = Auction.objects.create(
                title=auction_data['title'],
                description=auction_data['description'],
                start_date=datetime.strptime(auction_data['start_date'], '%Y-%m-%dT%H:%M:%SZ'),
                end_date=datetime.strptime(auction_data['end_date'], '%Y-%m-%dT%H:%M:%SZ'),
                initial_price=auction_data['initial_price'],
                shoe=shoe
            )
            self.stdout.write(self.style.SUCCESS(f"Created auction: {auction.title}"))
