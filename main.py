import requests
import re
import os

# Define the Listing class
class Listing:
    def __init__(self, rent, location, city):
        self.rent = rent
        self.location = location.strip()
        self.city = city.strip()

    # Define equality comparison method
    def __eq__(self, other):
        return (
            isinstance(other, Listing) and
            self.rent == other.rent and
            self.location == other.location and
            self.city == other.city
        )

    # Define hash method for hashing in sets
    def __hash__(self):
        return hash((self.rent, self.location, self.city))

# Function to save new listings to a file
def save_new_listings(listings):
    with open("listings.txt", "a") as file:
        for listing in listings:
            file.write(",".join(listing) + "\n")


# Function to load listings from a file
def load_listings():
    listings = []
    if os.path.exists("listings.txt"):
        with open("listings.txt", "r") as file:
            for line in file:
                listings.append(line.strip().split(","))
    return listings

radius = 10
min_size = 6
max_rent = 800
city = "utrecht"
page_suffix = "&typeAndCity=properties-utrecht&pageNo="
page_number = 1
url = "https://kamernet.nl/en/for-rent/properties-"+\
      city+"?radius="+str(radius)+"&maxRent="+str(max_rent/100)+\
      "&listingTypes=1%2C2%2C4%2C8&searchview=1"+\
      str(page_suffix)+str(page_number)
print(f"url used: {url}")
# Define the URL
# url = "https://kamernet.nl/en/for-rent/properties-utrecht?radius=5&minSize=6&maxRent=6&listingTypes=1%2C2%2C4%2C8&searchview=1"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use regex pattern to find rent, location, and city for both rooms and apartments
    rent_pattern = r'(?:Room|Apartment) for rent (\d+)\s+euro\s+([^,]+),\s+([^\d]+)'

    # Find all matches of rent pattern in response text
    new_listings = re.findall(rent_pattern, response.text)

    # Load previously saved listings and convert to Listing objects
    old_listings = [Listing(*listing) for listing in load_listings()]

    # Convert new listings to Listing objects
    new_listings = [Listing(*listing) for listing in new_listings]

    # Find new listings that are not in old listings
    new_listings_filtered = [listing for listing in new_listings if listing not in old_listings]

    if new_listings_filtered:
        # Send email with new listings
        # Implement email sending here (you mentioned you have it set up)

        # Print new listings
        print(f"New {len(new_listings_filtered)} listing(s) found:")
        for listing in new_listings_filtered:
            print("Rent:", listing.rent)
            print("Location:", listing.location)
            print("City:", listing.city)

    else:
        print("No new listings found")

    # Save all new listings to file for next run
    save_new_listings([listing.__dict__.values() for listing in new_listings_filtered])

else:
    print("Failed to retrieve the page. Status code:", response.status_code)
