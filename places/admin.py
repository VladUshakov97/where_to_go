from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html


class PlaceImageInline(admin.TabularInline):
	readonly_fields = ['image_preview']
	fields = ['image', 'image_preview', 'order']
	def image_preview(self, obj):
		if obj and obj.image:
			return format_html('<img src="{}" style="max-height: 200px; width: auto;">', obj.image.url)
		else:
			return 'Нет фотографии'
	model = PlaceImage


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
	inlines = [PlaceImageInline]