import time

import requests
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    def __str__(self):
        return f"Listing for {self.rent}€, in {self.location}, in {self.city}"

def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Gmail SMTP port

    # Create a message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message
    msg.attach(MIMEText(message, 'plain'))

    # Start the SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Log in to the SMTP server
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Quit the SMTP server
    server.quit()


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

# Get email credentials from environment variables
sender_email = os.environ.get('SENDER_EMAIL')
sender_password = os.environ.get('SENDER_PASSWORD')

receiver_email = os.environ.get('RECEIVER_EMAIL')
subject = "Kamernet bot update"


url = "https://kamernet.nl/en/for-rent/properties-"+\
      city+"?radius="+str(radius)+"&maxRent="+str(max_rent/100)+\
      "&listingTypes=1%2C2%2C4%2C8&searchview=1"+\
      str(page_suffix)+str(page_number)
print(f"url used: {url}")
# Define the URL
# url = "https://kamernet.nl/en/for-rent/properties-utrecht?radius=5&minSize=6&maxRent=6&listingTypes=1%2C2%2C4%2C8&searchview=1"

while True:
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
            message = f"New {len(new_listings_filtered)} listing(s) found:\n"
            for listing in new_listings_filtered:
                message += str(listing)
                message += "\n\n"


            if sender_email and sender_password:
                send_email(sender_email, sender_password, receiver_email, subject, message)
                print("Email sent successfully")
            else:
                print("Sender email or password not provided.")

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
    print("Waiting for 1 hour")
    time.sleep(3600)

