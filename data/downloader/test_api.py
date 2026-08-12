import requests

url = "https://pollution.gov.np/gss/api/observation"

params = {
    "series_id": 523,
    "date_from": "2026-07-01T00:00:00",
    "date_to": "2026-08-12T00:00:00",
}

response = requests.get(
    url,
    params=params,
    timeout=60,
)

print("Status:", response.status_code)
print("URL:", response.url)

data = response.json()

print("\nResponse type:")
print(type(data))

print("\nResponse:")
print(data)

if isinstance(data, list):
    print("\nNumber of items:", len(data))

    if len(data) > 0:
        print("\nFirst item:")
        print(data[0])

        print("\nLast item:")
        print(data[-1])
