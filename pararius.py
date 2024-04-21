import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Define the Listing class
class Listing:
    def __init__(self, name, address, price, size, rooms, furnishment):
        self.name = name
        self.address = address
        self.price = price
        self.size = size
        self.rooms = rooms
        self.furnishment = furnishment

    def __eq__(self, other):
        return (
            isinstance(other, Listing) and
            self.name == other.name and
            self.address == other.address
        )

    def __hash__(self):
        return hash((self.name, self.address))

    def __str__(self):
        return f"{self.name} - {self.address}\nPrice: {self.price}\nSize: {self.size} sqm\nRooms: {self.rooms}\nFurnishment: {self.furnishment}"

# Function to save new Pararius listings to a file
def save_new_pararius_listings(listings):
    with open("pararius.txt", "a") as file:
        for listing in listings:
            file.write(";".join(listing.__dict__.values()) + "\n")

# Function to load Pararius listings from a file
def load_pararius_listings():
    listings = []
    if os.path.exists("pararius.txt"):
        with open("pararius.txt", "r") as file:
            for line in file:
                data = line.strip().split(";")
                listing = Listing(*data)
                listings.append(listing)
    return listings

def scrape_pararius():
    url = 'https://www.pararius.com/apartments/utrecht'

    # Add Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Pass options when creating driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)

    listings = driver.find_elements(By.CLASS_NAME, 'search-list__item--listing')
    scraped_listings = []

    for listing in listings:
        lines = listing.text.split('\n')
        name = lines[1]
        address = lines[2]
        price = lines[3]
        size = lines[4]
        rooms = lines[5]
        furnishment = lines[6]

        listing = Listing(name, address, price, size, rooms, furnishment)
        scraped_listings.append(listing)

    driver.quit()
    return scraped_listings

def run(send_email):
    # Load existing Pararius listings
    old_listings = load_pararius_listings()

    # Scrape new Pararius listings
    new_listings = scrape_pararius()

    # Find new Pararius listings that are not in old listings
    new_listings_filtered = [listing for listing in new_listings if listing not in old_listings]

    if new_listings_filtered:
        # Save new Pararius listings to file
        save_new_pararius_listings(new_listings_filtered)

        # Send email with all new Pararius listings
        message = "New Pararius listings found:\n"
        for listing in new_listings_filtered:
            message += str(listing)
            message += "\n\n"

        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        receiver_emails = os.environ.get('RECEIVER_EMAIL').split(',')
        subject = "Pararius bot update"

        if sender_email and sender_password:
            for receiver_email in receiver_emails:
                send_email(sender_email, sender_password, receiver_email, subject, message)
            print("Email sent successfully")
        else:
            print("Sender email or password not provided.")

        # Print new Pararius listings
        print(f"New {len(new_listings_filtered)} Pararius listing(s) found:")
        for listing in new_listings_filtered:
            print(listing)
    else:
        print("No new Pararius listings found")
