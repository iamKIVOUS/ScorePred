from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import re

# Paths
csv_file = "data/ipl_full_scorecard_links.csv"
output_csv_path = "data/bowler_data.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Load all match URLs from file
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    urls = [row["scorecard_url"] for row in reader]

# Load already processed match_ids
processed_match_ids = set()
if os.path.exists(output_csv_path):
    with open(output_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed_match_ids.add(row["match_id"])

# Prepare CSV for appending new records
write_header = not os.path.exists(output_csv_path)
csv_out = open(output_csv_path, "a", newline='', encoding="utf-8")
writer = csv.DictWriter(csv_out, fieldnames=[
    "match_id", "player_id", "player_name", "team_id",
    "runs_conceded", "total_overs", "economy", "dots",
    "wickets", "fours", "sixes", "wide", "no_balls",
])
if write_header:
    writer.writeheader()

# Selenium setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 7)

# Utility to safely extract text using XPath
def get_text(xpath):
    try:
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
    except:
        return "N/A"

# Main scraping loop
for j, url in enumerate(urls, 1):
    match_id = url.split("/")[-2].split("-")[-1]

    if match_id in processed_match_ids:
        print(f"[{j}/{len(urls)}] Skipping already scraped match: {match_id}")
        continue

    print(f"[{j}/{len(urls)}] Scraping new match: {url}")
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    for div_index in [2, 3]:
        team_name_xpath = f'//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[{5 - div_index}]/div/div[1]/div/span/span[1]'
        team_name = get_text(team_name_xpath)

        rows_xpath = f'//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[{div_index}]/div/div[2]/table[2]/tbody/tr'
        rows = driver.find_elements(By.XPATH, rows_xpath)

        for i, row in enumerate(rows, 1):
            try:
                if any(td.get_attribute("colspan") for td in row.find_elements(By.TAG_NAME, "td")):
                    continue

                player_anchor = row.find_element(By.XPATH, f"./td[1]/div/div/a")
                player_name = player_anchor.find_element(By.XPATH, f"./span").text.strip()
                player_href = player_anchor.get_attribute("href")
                player_id = player_href.split("/")[-1]

                player_data = {
                    "match_id": match_id,
                    "player_id": player_id.split("-")[-1],
                    "player_name": re.sub(r"\s*[\(].*?[\)]|\s*†", "", player_name).strip(),
                    "team_id": team_name,
                    "runs_conceded": get_text(f'({rows_xpath})[{i}]/td[4]'),
                    "total_overs": get_text(f'({rows_xpath})[{i}]/td[2]'),
                    "economy": get_text(f'({rows_xpath})[{i}]/td[6]'),
                    "dots": get_text(f'({rows_xpath})[{i}]/td[7]'),
                    "wickets": get_text(f'({rows_xpath})[{i}]/td[5]//strong'),
                    "fours": get_text(f'({rows_xpath})[{i}]/td[8]'),
                    "sixes": get_text(f'({rows_xpath})[{i}]/td[9]'),
                    "wide": get_text(f'({rows_xpath})[{i}]/td[10]'),
                    "no_balls": get_text(f'({rows_xpath})[{i}]/td[11]'),
                }

                writer.writerow(player_data)
                print(f"Saved: {player_data['player_name']}")

            except Exception as e:
                print(f"Error processing row {i}: {e}")
                continue

driver.quit()
csv_out.close()
print("Scraping complete.")
