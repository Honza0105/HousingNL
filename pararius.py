from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

url = 'https://www.pararius.com/apartments/utrecht'

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)

listings = driver.find_elements(By.CLASS_NAME, 'search-list__item--listing')

for listing in listings:

  try:
    price = listing.find_element(By.CLASS_NAME, 'listing-search-item__price').text
  except NoSuchElementException:
    price = "N/A"

  try:
    features = listing.find_elements(By.CLASS_NAME, 'illustrated-features__item')
  except NoSuchElementException:
    features = []

  print(price)

  for feature in features:
    print(feature.text)

driver.close()
