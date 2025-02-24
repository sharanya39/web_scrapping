import os
import time
import requests
import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Create folder to store images
output_folder = "ThalapathyVijay_HDimages"
os.makedirs(output_folder, exist_ok=True)

# Set up Chrome in headless mode (Runs in background)
options = Options()
options.add_argument("--headless")  # No GUI
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# List of search queries to collect 1000+ images
search_queries = [
    "Actor Thalapathy Vijay HD photos",
#"Vijay Tamil actor latest images",
    #"Thalapathy Vijay movie stills",
    #"Vijay photoshoot pictures",
    #"Vijay smiling photos",
    #"Vijay wallpaper images",
    #"Vijay latest movie scenes"
]

image_urls = set()

# Loop through multiple search queries
for query in search_queries:
    print(f"Searching for: {query}")
    google_images_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    driver.get(google_images_url)
    time.sleep(3)  # Wait for images to load

    # Click "Show more results" button if available
    try:
        while True:
            show_more_button = driver.find_element(By.XPATH, "//input[@value='Show more results']")
            show_more_button.click()
            time.sleep(3)
    except:
        pass  # If button not found, continue

    # Scroll multiple times to load more images
    for _ in range(30):  # Adjust this for more images
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    # Extract image URLs
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        src = img.get_attribute("src")
        if src and "http" in src:
            image_urls.add(src)

driver.quit()  # Close the browser
print(f"Total images found: {len(image_urls)}")

# Download images asynchronously
async def download_image(session, url, filename):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, "wb") as file:
                    file.write(await response.read())
    except Exception as e:
        print(f"Failed to download {url}: {e}")

async def download_all_images():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(image_urls):
            filename = f"{output_folder}/vijay_{i}.jpg"
            tasks.append(download_image(session, url, filename))
        await asyncio.gather(*tasks)

# Run the async function to download images
asyncio.run(download_all_images())

print(f"Downloaded {len(image_urls)} images to '{output_folder}'")
