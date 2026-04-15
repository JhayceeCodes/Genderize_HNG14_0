import requests
from django.http import JsonResponse
from rest_framework import status
from django.utils import timezone


def classify_name(request):
    name = request.GET.get("name")

    if not name:
        return JsonResponse({"status": "error",
                             "message": "Name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not name.isalpha():
        return JsonResponse({"status": "error",
                             "message": "Name must contain only letters"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    try:
        response = requests.get("https://api.genderize.io", 
                                params={"name": name})
        

        if response.status_code >= 500:
            return JsonResponse({
                "status": "error",
                "message": "Upstream service unavailable"
            }, status=status.HTTP_502_BAD_GATEWAY)

        api_data = response.json()

        gender = api_data.get("gender")
        sample_size = api_data.get("count")
        probability = api_data.get("probability")
        processed_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")


        is_confident = (
            probability is not None and
            sample_size is not None and
            probability >= 0.7 and
            sample_size >= 100
        )

        if gender is None or sample_size in (None, 0):
            return JsonResponse({"status": "error",
                             "message": "No prediction available for the provided name"}, 
                             status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        new_response = {
                        "status": "success",
                        "data": {
                            "name": name,
                            "gender": gender,
                            "probability": probability,
                            "sample_size": sample_size,
                            "is_confident": is_confident,
                            "processed_at": processed_at
                        }    
                    }

        return JsonResponse(new_response)
    
    except requests.Timeout:
        return JsonResponse({
            "status": "error",
            "message": "Upstream request timed out"
        }, status=status.HTTP_502_BAD_GATEWAY)

    except requests.RequestException:
        return JsonResponse({
            "status": "error",
            "message": "Failed to fetch data from external API"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

