from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from places.models import Place, PlaceImage


class Command(BaseCommand):
	def handle(self, *args, **options):
		value = options['url']
		response = requests.get(value)
		response.raise_for_status()
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
				image_response.raise_for_status()
				filename = image.split('/')[-1]
				image_file = ContentFile(image_response.content, name=filename)
				PlaceImage.objects.create(place=place, image=image_file)


	def add_arguments(self, parser):
		parser.add_argument('url')