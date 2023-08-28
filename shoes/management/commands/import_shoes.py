import json
from django.core.management.base import BaseCommand
from shoes.models import Shoe

class Command(BaseCommand):
    help = 'Import shoes from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        with open(json_file_path, 'r', encoding='utf-8') as file:
            shoes_data = json.load(file)

        for shoe_data in shoes_data:
            shoe = Shoe.objects.create(
                name=shoe_data['name'],
                image=shoe_data['image'],
                description=shoe_data['description'],
                color=shoe_data['color']
            )
            self.stdout.write(self.style.SUCCESS(f"Created shoe: {shoe.name}"))
