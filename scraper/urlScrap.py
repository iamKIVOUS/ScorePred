
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import csv

# Path to output CSV
output_path = os.path.join(os.path.dirname(__file__), "../data/ipl_full_scorecard_links.csv")
output_path = os.path.abspath(output_path)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Load existing URLs into a set
existing_urls = set()
if os.path.exists(output_path):
    with open(output_path, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            if row:
                existing_urls.add(row[0])

# Selenium setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 7)

# Season URLs
season_urls = [
    "https://www.espncricinfo.com/series/indian-premier-league-2007-08-313494/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2009-374163/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2009-10-418064/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2011-466304/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2012-520932/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2013-586733/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/pepsi-indian-premier-league-2014-695871/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/ipl-2016-968923/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/ipl-2017-1078425/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/ipl-2018-1131611/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/ipl-2019-1165643/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/ipl-2021-1249214/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/indian-premier-league-2024-1410320/match-schedule-fixtures-and-results",
    "https://www.espncricinfo.com/series/ipl-2025-1449924/match-schedule-fixtures-and-results"
]

new_links = []

for url in season_urls:
    print(f"Opening URL: {url}")
    driver.get(url)
    try:
        anchors = wait.until(EC.presence_of_all_elements_located((
            By.XPATH,
            '//*[@id="main-container"]/div[5]/div/div[4]/div[1]/div[1]/div/div/div/div/div/div[2]/a'
        )))
        print("Extracted hrefs")
        for a in anchors:
            href = a.get_attribute("href")
            if href and href.endswith("/full-scorecard") and href not in existing_urls:
                new_links.append([href])
                existing_urls.add(href)
    except Exception as e:
        print("Error extracting hrefs:", e)

driver.quit()

# Append new links to CSV
if new_links:
    write_header = not os.path.exists(output_path)
    with open(output_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["scorecard_url"])
        writer.writerows(new_links)
    print(f"{len(new_links)} new URLs added.")
else:
    print("No new URLs found. CSV is up to date.")
