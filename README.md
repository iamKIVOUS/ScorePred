
# scorePred 🏏

A Django-based IPL score prediction and data analysis tool using scraped data from ESPNcricinfo.

## Features
- Scrapes latest IPL match, batter, and bowler data.
- Imports scraped data into Django models.

## Project Structure
- `scraper/`: Contains all scraping scripts
- `backend/`: Django app with models and admin
- `data/`: Stores CSV data files

## Setup
1. Clone the repo
2. Create a virtual environment and activate it
    venv\Scripts\activate    
    # if facing error
    # try
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\venv\Scripts\Activate.ps1
3. Install dependencies:
    pip install -r requirements.txt
4. run scraper/automator.py
    python scrape/automator.py

## ML training will be added later