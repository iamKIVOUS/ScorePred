from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import re

csv_file = "data/ipl_full_scorecard_links.csv"
# URL of the match
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    urls = [row["scorecard_url"] for row in reader]
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 7)
match_over_links = []
for i, url in enumerate(urls, 1):
    print(f"Opening [{i}/{len(urls)}]: {url}")
    driver.get(url)
    try:
        # Get all <a> elements matching the pattern using XPath wildcard
        anchors = wait.until(EC.presence_of_all_elements_located((
            By.XPATH,
            '//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[1]/div/div[2]/div/div[7]/a'
        )))

    # Loop through and print hrefs
        print("Extracted hrefs:")
        for i, a in enumerate(anchors, 1):
            href = a.get_attribute("href")
            if href:
                match_over_links.append([href])


    except Exception as e:
        print("Error extracting hrefs:", e)


output_path = os.path.join(os.path.dirname(__file__), "../data/match_over_links.csv")

# Normalize path to absolute
output_path = os.path.abspath(output_path)

# Ensure parent directory exists (optional safety)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["match_over_url"])
    writer.writerows(match_over_links)
driver.quit()