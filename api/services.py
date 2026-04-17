import requests

BASE_TIMEOUT = 5


class ExternalAPIError(Exception):
    def __init__(self, api_name):
        self.api_name = api_name
        super().__init__(api_name)


def genderize(name):
    res = requests.get("https://api.genderize.io", params={"name": name}, timeout=BASE_TIMEOUT)
    data = res.json()

    if res.status_code >= 500 or data.get("gender") is None or data.get("count") in (None, 0):
        raise ExternalAPIError("Genderize")

    return {
        "gender": data["gender"],
        "probability": round(data["probability"], 2),
        "count": data["count"]
    }


def agify(name):
    res = requests.get("https://api.agify.io", params={"name": name}, timeout=BASE_TIMEOUT)
    data = res.json()

    if res.status_code >= 500 or data.get("age") is None:
        raise ExternalAPIError("Agify")

    return {"age": data["age"]}


def nationalize(name):
    res = requests.get("https://api.nationalize.io", params={"name": name}, timeout=BASE_TIMEOUT)
    data = res.json()

    countries = data.get("country")

    if res.status_code >= 500 or not countries:
        raise ExternalAPIError("Nationalize")

    best = max(countries, key=lambda x: x["probability"])

    return {
        "country_id": best["country_id"],
        "probability": round(best["probability"], 2)
    }