import requests

def get_country_info(country_name):
    """
    Fetch information about a country by its name.
    """
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        response.raise_for_status()
        data = response.json()[0]
        
        info = {
            "Name": data.get("name", {}).get("common", "N/A"),
            "Capital": data.get("capital", ["N/A"])[0],
            "Region": data.get("region", "N/A"),
            "Population": data.get("population", "N/A"),
            "Currencies": list(data.get("currencies", {}).keys()),
            "Languages": list(data.get("languages", {}).values())
        }
        return str(info)
    except Exception as e:
        return f"Error fetching country info: {e}"