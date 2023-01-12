
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getLocationQuery(request) -> None:
    if request.method == "POST":
        data = request.POST
        latitude = data["latitude"]
        longitude = data["longitude"]
        x = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{longitude},{latitude}.json?access_token=pk.eyJ1Ijoicnl1aW53MTIzIiwiYSI6ImNsODV5M21odjB0dXAzbm9lZDhnNXVoY2UifQ.IiTAr5ITOUcCVjPjWiRe1w&limit=1")
        data = x.json()

        if (data["features"]):
            feature = data["features"][0]

            response = {
                "place" : feature["text"],
                "address" : feature["place_name"]
            }
        else:
            response = {
                "place" : "The Ocean",
                "address" : " "
            }
        

        return JsonResponse(response,safe=False)