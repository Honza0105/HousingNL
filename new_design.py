import time

import requests
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Listing:
    def __init__(self, rent, location, city):
        self.rent = rent
        self.location = location.strip()
        self.city = city.strip()

    def __eq__(self, other):
        return (
            isinstance(other, Listing) and
            self.rent == other.rent and
            self.location == other.location and
            self.city == other.city
        )

    def __hash__(self):
        return hash((self.rent, self.location, self.city))

    def __str__(self):
        return f"Listing for {self.rent}€, in {self.location}, in {self.city}"

def send_email(sender_email, sender_password, receiver_email, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

def save_new_listings(listings):
    with open("listings.txt", "a") as file:
        for listing in listings:
            file.write(",".join(listing) + "\n")

def load_listings():
    listings = []
    if os.path.exists("listings.txt"):
        with open("listings.txt", "r") as file:
            for line in file:
                listings.append(line.strip().split(","))
    return listings

radius = 10
max_rent = 800
city = "utrecht"
page_suffix = "&typeAndCity=properties-utrecht&pageNo="
page_number = 1

sender_email = os.environ.get('SENDER_EMAIL')
sender_password = os.environ.get('SENDER_PASSWORD')
receiver_email = os.environ.get('RECEIVER_EMAIL')
subject = "Kamernet bot update"

while True:
    new_listings_filtered = []
    page_number = 1

    while True:
        url = "https://kamernet.nl/en/for-rent/properties-" + city + "?radius=" + str(radius) + "&maxRent=" + str(max_rent / 100) + "&listingTypes=1%2C2%2C4%2C8&searchview=1" + str(page_suffix) + str(page_number)
        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to retrieve the page. Status code:", response.status_code)
            break

        rent_pattern = r'€ (\d+),-\n\s+([^<]+)\n\s+([^\n]+)'

        new_listings = re.findall(rent_pattern, response.text)
        old_listings = [Listing(*listing) for listing in load_listings()]
        new_listings = [Listing(*listing) for listing in new_listings]

        new_listings_filtered.extend([listing for listing in new_listings if listing not in old_listings])

        if not new_listings:
            break

        page_number += 1

    if new_listings_filtered:
        save_new_listings([listing.__dict__.values() for listing in new_listings_filtered])

        message = "New listings found:\n"
        for listing in new_listings_filtered:
            message += str(listing)
            message += "\n\n"

        if sender_email and sender_password:
            send_email(sender_email, sender_password, receiver_email, subject, message)
            print("Email sent successfully")
        else:
            print("Sender email or password not provided.")

        print(f"New {len(new_listings_filtered)} listing(s) found:")
        for listing in new_listings_filtered:
            print("Rent:", listing.rent)
            print("Location:", listing.location)
            print("City:", listing.city)

    else:
        print("No new listings found")

    print("Waiting for half an hour before checking for new listings again")
    time.sleep(1800)
