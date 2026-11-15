from django.db import models
from tinymce.models import HTMLField

class Place(models.Model):
	title = models.CharField(max_length=200, verbose_name='Название')
	short_description = models.TextField(verbose_name='Короткое описание', blank=True)
	long_description = HTMLField(verbose_name='Длинное описание', blank=True)
	lon = models.FloatField(verbose_name='Долгота')
	lat = models.FloatField(verbose_name='Широта')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural ='Место'


class PlaceImage(models.Model):
	place = models.ForeignKey(
		Place,
		on_delete=models.CASCADE,
		related_name='images',
		verbose_name='Локация')

	image = models.ImageField(upload_to='places/', verbose_name='Картинка')
	order = models.PositiveIntegerField(default=0, db_index=True, verbose_name='Порядок отображения фотографий')

	def __str__(self):
		return f'{self.order} {self.place.title}'

	class Meta:
		ordering = ['order']
		verbose_name_plural = 'Фотографии'

