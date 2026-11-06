from django.db import models

# Create your models here.
class Place(models.Model):
	title = models.CharField(max_length=200)
	description_short = models.TextField()
	description_long = models.TextField()
	lon = models.FloatField()
	lat = models.FloatField()


	def __str__(self):
		return self.title


class PlaceImage(models.Model):
	place = models.ForeignKey(
		Place,
		on_delete=models.CASCADE,
		related_name='images')

	image = models.ImageField(upload_to='places/')
	order = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f'{self.order} {self.place.title}'

	class Meta:
		ordering = ['order']

