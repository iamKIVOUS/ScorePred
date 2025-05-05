from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

input_csv = "data/ipl_full_scorecard_links.csv"
output_csv = "data/match_data.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Step 1: Load existing match IDs from match_data.csv if it exists
existing_match_ids = set()
if os.path.exists(output_csv):
    with open(output_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_match_ids.add(row["match_id"])

# Step 2: Read URLs and extract match_ids from them
new_urls = []
with open(input_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row["scorecard_url"]
        match_id = url.split("/")[-2].split("-")[-1]
        if match_id not in existing_match_ids:
            new_urls.append((url, match_id))

# Exit early if no new URLs
if not new_urls:
    print("No new URLs to scrape.")
    exit()

# Step 3: Prepare output CSV
write_header = not os.path.exists(output_csv)
csv_out = open(output_csv, "a", newline='', encoding="utf-8")
writer = csv.DictWriter(csv_out, fieldnames=[
    "match_id", "date", "season", "venue",
    "toss_winner", "toss_decision",
    "team_1", "team_2",
    "team_1_score", "team_1_wicket",
    "team_2_score", "team_2_wicket",
    "winner", "loser",
    "player_of_the_match", "umpire_1", "umpire_2"
])
if write_header:
    writer.writeheader()

# Step 4: Start Selenium
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 7)

def get_text(xpath):
    try:
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
    except:
        return "N/A"

# Step 5: Scrape only new matches
for i, (url, match_id) in enumerate(new_urls, 1):
    print(f"Scraping [{i}/{len(new_urls)}]: {url}")
    driver.get(url)
    time.sleep(5)

    data = {
        "match_id": match_id,
        "date": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[7]/td[2]/span'),
        "season": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[4]/td[2]/a/span'),
        "venue": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[1]/td/a/span'),
        "toss_winner": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[2]/td[2]/span'),
        "toss_decision": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[2]/td[2]/span'),
        "team_1": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/span/span[1]'),
        "team_2": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div/span/span[1]'),
        "team_1_score": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/strong'),
        "team_2_score": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/strong'),
        "player_of_the_match": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[5]/td[2]/div/a/span/span'),
        "umpire_1": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[9]/td[2]/div[1]/a/span/span'),
        "umpire_2": get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[9]/td[2]/div[2]/a/span/span'),
    }

    data["date"] = data["date"].split(" - ")[0].strip()
    data["toss_winner"] = data["toss_winner"].split(",")[0].strip()
    data["toss_decision"] = "bat" if "bat" in data["toss_decision"].split(",")[1] else "field"

    data["team_1_score"], data["team_1_wicket"] = map(int, data["team_1_score"].split("/")) if "/" in data["team_1_score"] else (int(data["team_1_score"]), 10)
    data["team_2_score"], data["team_2_wicket"] = map(int, data["team_2_score"].split("/")) if "/" in data["team_2_score"] else (int(data["team_2_score"]), 10)
    data["winner"], data["loser"] = (data["team_1"], data["team_2"]) if data["team_1_score"] > data["team_2_score"] else (data["team_2"], data["team_1"])
    data["season"] = data["season"][:2] + data["season"][-2:] if "/" in data["season"] else data["season"]

    # Alternate umpire location check
    if data["umpire_2"] == "N/A":
        data["umpire_1"] = get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[8]/td[2]/div[1]/a/span/span')
        data["umpire_2"] = get_text('//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody/tr[8]/td[2]/div[2]/a/span/span')

    writer.writerow(data)

# Cleanup
csv_out.close()
driver.quit()
print(f"Scraping complete. {len(new_urls)} new matches added.")
