import requests

def calculator(a, b, operation):
    """
    Simple calculator tool.
    a, b -> numbers
    operation -> add, sub, mul, div
    """
    if operation == "add":
        return str(a + b)
    elif operation == "sub":
        return str(a - b)
    elif operation == "mul":
        return str(a * b)
    elif operation == "div":
        if b == 0:
            return "Error: Division by zero"
        return str(a / b)
    else:
        return "Error: Unknown operation"

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