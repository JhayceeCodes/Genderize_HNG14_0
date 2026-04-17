from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .services import genderize, agify, nationalize, ExternalAPIError
from .utils import get_age_group, format_profile, format_profile_list


class ProfileView(APIView):

    def post(self, request):
        name = request.data.get("name")

        if not name:
            return Response(
                {"status": "error", "message": "Missing or empty name"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(name, str):
            return Response(
                {"status": "error", "message": "Invalid type"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if not name.isalpha():
            return Response(
                {"status": "error", "message": "Name must contain only letters"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        name = name.lower()


        existing = Profile.objects.filter(name=name).first()
        if existing:
            return Response({
                "status": "success",
                "message": "Profile already exists",
                "data": format_profile(existing)
            })

        try:
            g = genderize(name)
            a = agify(name)
            n = nationalize(name)

        except ExternalAPIError as e:
            return Response({
                "status": "error",
                "message": f"{e.api_name} returned an invalid response"
            }, status=status.HTTP_502_BAD_GATEWAY)



        profile = Profile.objects.create(
            name=name,
            gender=g["gender"],
            gender_probability=g["probability"],
            sample_size=g["count"],
            age=a["age"],
            age_group=get_age_group(a["age"]),
            country_id=n["country_id"],
            country_probability=n["probability"],
        )

        return Response({
            "status": "success",
            "data": format_profile(profile)
        }, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        profiles = Profile.objects.all()

        gender = request.GET.get("gender")
        country = request.GET.get("country_id")
        age_group = request.GET.get("age_group")

        if gender:
            profiles = profiles.filter(gender__iexact=gender)

        if country:
            profiles = profiles.filter(country_id__iexact=country)

        if age_group:
            profiles = profiles.filter(age_group__iexact=age_group)

        data = [format_profile_list(p) for p in profiles]

        return Response({
            "status": "success",
            "count": len(data),
            "data": data
        })
    



class ProfileDetailView(APIView):
    def get_object(self, id):
        try:
            return Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return None


    def get(self, request, id):
        profile = self.get_object(id)

        if not profile:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "status": "success",
            "data": format_profile(profile)
        })


    def delete(self, request, id):
        profile = self.get_object(id)

        if not profile:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)