from django.shortcuts import render
from django.templatetags.static import static
from .models import Place
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse


# Create your views here.
def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    images = place.images.all()
    image_urls = []
    for image in images:
        image_urls.append(image.image.url)
    place_data = {
        'title': place.title,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'imgs': image_urls,
        'coordinates': {
            'lng': place.lon,
            'lat': place.lat,
        }
    }

    return JsonResponse(place_data)


def index(request):
    places = Place.objects.all()
    places_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for place in places:
        place_data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lon, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': reverse('place_detail', args=[place.id]),
            }
        }
        places_geojson['features'].append(place_data)
    print(place.lon, place.lat)

    context = {
        'places_geojson': places_geojson,
    }

    return render(request, 'index.html', context)


    #         {
    #             "type": "Feature",
    #             "geometry": {
    #                 "type": "Point",
    #                 "coordinates": [37.62, 55.793676]
    #             },
    #             "properties": {
    #                 "title": "«Легенды Москвы",
    #                 "placeId": "moscow_legends",
    #                 "detailsUrl": static('places/moscow_legends.json')
    #             }
    #         },
    #         {
    #             "type": "Feature",
    #             "geometry": {
    #                 "type": "Point",
    #                 "coordinates": [37.64, 55.753676]
    #             },
    #             "properties": {
    #                 "title": "Крыши24.рф",
    #                 "placeId": "roofs24",
    #                 "detailsUrl": static('places/roofs24.json')
    #             }
    #         }
    #     ]
    # }

    