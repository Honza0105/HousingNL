import requests
import re

# Define the URL
url = "https://kamernet.nl/en/for-rent/properties-utrecht?radius=5&minSize=6&maxRent=6&listingTypes=1%2C2%2C4%2C8&searchview=1"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use regex pattern to find rent and location
    rent_pattern = r'Room for rent (\d+)\s+euro\s+([^\d]+),\s+([^\d]+)'

    # Find all matches of rent pattern in response text
    matches = re.findall(rent_pattern, response.text)

    # Print out the number of matches
    print("Number of listings found:", len(matches))

    # Print out the extracted rents and locations
    for match in matches:
        rent, location, city = match
        print("Rent:", rent)
        print("Location:", location)
        print("City:", city)

else:
    print("Failed to retrieve the page. Status code:", response.status_code)
