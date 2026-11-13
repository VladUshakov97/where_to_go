from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from places.models import Place, PlaceImage


class Command(BaseCommand):
	def handle(self, *args, **options):
		value = options['url']
		response = requests.get(value)
		place_data = response.json()
		longitude = float(place_data['coordinates']['lng'])
		latitude = float(place_data['coordinates']['lat'])
		title = place_data['title']
		place, created = Place.objects.get_or_create(
			title=title,
			defaults={
			    'lon': longitude,
			    'lat': latitude,
			    'description_short': place_data['description_short'],
			    'description_long': place_data['description_long']
			}
		)

		if created:
			for image in place_data['imgs']:
				image_response = requests.get(image)
				image_file = ContentFile(image_response.content)
				place_image = PlaceImage(place=place)
				name = image.split('/')
				filename = name[-1]
				place_image.image.save(filename, image_file)


	def add_arguments(self, parser):
		parser.add_argument('url')