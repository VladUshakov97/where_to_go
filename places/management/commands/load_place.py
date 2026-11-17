import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from places.models import Place, PlaceImage


class Command(BaseCommand):
	def handle(self, *args, **options):
		value = options['url']
		try:
		    response = requests.get(value)
		    response.raise_for_status()
		except requests.exceptions.RequestException as error:
		    raise CommandError(
		    	f'Ошибка загрузки JSON, {value}: {error}'
		    ) from error
		place_data = response.json()
		longitude = float(place_data['coordinates']['lng'])
		latitude = float(place_data['coordinates']['lat'])
		title = place_data['title']
		place, created = Place.objects.get_or_create(
			title=title,
			defaults={
			    'lon': longitude,
			    'lat': latitude,
			    'short_description': place_data['short_description'],
			    'long_description': place_data['long_description']
			}
		)

		if created:
			for image in place_data['imgs']:
				try:
				    image_response = requests.get(image)
				    image_response.raise_for_status()
				except requests.exceptions.RequestException as error:
					raise CommandError(
						f'Ошибка загрузки фотографий, {image}: {error}'
					) from error
				filename = image.split('/')[-1]
				image_file = ContentFile(image_response.content, name=filename)
				PlaceImage.objects.create(place=place, image=image_file)
			self.stdout.write('Локация успешно создана')
		else:
			self.stdout.write('Локация уже существует')


	def add_arguments(self, parser):
		parser.add_argument('url')