from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import re

# --- File paths ---
scorecard_csv = "data/ipl_full_scorecard_links.csv"
output_csv = "data/batter_data.csv"

# --- Read all URLs from source CSV ---
with open(scorecard_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    urls = [row["scorecard_url"] for row in reader]

# --- Prepare output directory ---
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# --- Track previously scraped match_ids ---
existing_match_ids = set()
if os.path.exists(output_csv):
    with open(output_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_match_ids.add(row["match_id"])

# --- Setup CSV writer ---
write_header = not os.path.exists(output_csv)
csv_out = open(output_csv, "a", newline='', encoding="utf-8")
writer = csv.DictWriter(csv_out, fieldnames=[
    "match_id", "player_id", "player_name", "team_id", "batting_position",
    "runs_scored", "balls_faced", "strike_rate", "fours", "sixes",
    "how_out", "bolwer_id"
])
if write_header:
    writer.writeheader()

# --- Selenium Setup ---
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 7)

def get_text(xpath):
    try:
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
    except:
        return "N/A"

# --- Start scraping new matches only ---
for j, url in enumerate(urls, 1):
    match_id = url.split("/")[-2].split("-")[-1]
    if match_id in existing_match_ids:
        print(f"[{j}/{len(urls)}] Skipping already scraped match: {match_id}")
        continue

    print(f"[{j}/{len(urls)}] Scraping: {url}")
    driver.get(url)
    time.sleep(5)

    for div_index in [2, 3]:  # Two teams

        team_name_xpath = f'//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[{div_index}]/div/div[1]/div/span/span[1]'
        team_name = get_text(team_name_xpath)

        rows_xpath = f'//*[@id="main-container"]/div[5]/div/div/div[3]/div[1]/div[2]/div[1]/div[{div_index}]/div/div[2]/table[1]/tbody/tr'
        rows = driver.find_elements(By.XPATH, rows_xpath)

        count = 1  # Batting position
        for i, row in enumerate(rows, 1):
            try:
                if any(td.get_attribute("colspan") for td in row.find_elements(By.TAG_NAME, "td")):
                    continue  # Skip non-player rows

                player_anchor = row.find_element(By.XPATH, f"./td[1]/div/div/a")
                player_name = player_anchor.find_element(By.XPATH, f"./span/span").text.strip()
                player_href = player_anchor.get_attribute("href")
                player_id = player_href.split("/")[-1].split("-")[-1]

                how_out = get_text(f'({rows_xpath})[{i}]/td[2]')
                runs = get_text(f'({rows_xpath})[{i}]/td[3]/strong')
                balls = get_text(f'({rows_xpath})[{i}]/td[4]')
                fours = get_text(f'({rows_xpath})[{i}]/td[6]')
                sixes = get_text(f'({rows_xpath})[{i}]/td[7]')
                sr = get_text(f'({rows_xpath})[{i}]/td[8]')

                cleaned_how_out = (
                    "lbw" if "lbw" in how_out else
                    "c" if "c " in how_out else
                    "rn" if "run out" in how_out else
                    "b" if how_out.startswith("b ") else
                    how_out
                )
                bolwer_id = how_out.split(" ")[-1] if "b " in how_out else "N/A"

                player_data = {
                    "match_id": match_id,
                    "player_id": player_id,
                    "player_name": re.sub(r"\s*[\(].*?[\)]|\s*†", "", player_name).strip(),
                    "team_id": team_name,
                    "batting_position": count,
                    "runs_scored": runs,
                    "balls_faced": balls,
                    "strike_rate": sr,
                    "fours": fours,
                    "sixes": sixes,
                    "how_out": cleaned_how_out,
                    "bolwer_id": bolwer_id
                }

                writer.writerow(player_data)
                print(f"Saved: {player_data['player_name']}")
                count += 1

            except Exception as e:
                print(f"Error processing row {i}: {e}")
                continue

driver.quit()
csv_out.close()
