from django.db import models

# Create your models here.
class Place(models.Model):
	title = models.CharField(max_length=200, verbose_name='Название')
	description_short = models.TextField(verbose_name='Короткое описание')
	description_long = models.TextField(verbose_name='Длинное описание')
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
		related_name='images')

	image = models.ImageField(upload_to='places/', verbose_name='Картинка')
	order = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f'{self.order} {self.place.title}'

	class Meta:
		ordering = ['order']
		verbose_name_plural ='Фотографии'

