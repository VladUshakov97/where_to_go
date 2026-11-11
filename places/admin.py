from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html
from adminsortable2.admin import SortableTabularInline, SortableAdminBase


class PlaceImageInline(SortableTabularInline):
	extra = 0
	readonly_fields = ['image_preview']
	fields = ['image', 'image_preview']
	def image_preview(self, obj):
		if obj and obj.image:
			return format_html('<img src="{}" style="max-height: 200px; width: auto;">', obj.image.url)
		else:
			return 'Нет фотографии'
	model = PlaceImage


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
	inlines = [PlaceImageInline]