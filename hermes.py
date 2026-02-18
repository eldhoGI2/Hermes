#!/usr/bin/env python3
import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# --- CONFIGURATION ---
VERSION = "3.1.0 (Banner Edition)"
DELAY = 1.5  # Safety delay to prevent blocking

# --- ASCII ART BANNER ---
BANNER = """
\033[1;34m

██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗
██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝
███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗
██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║
██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
                                                   
\033[0m      \033[1;37mv3.1 - The Ultimate Scraper\033[0m
"""

# Sites that host BOTH Movies and TV Series
URLS = [
    "https://hdtodayz.uk",
    "https://wvv-fmovies.com/home/",
    "https://ww25.soap2day.day/soap2day-r26n8/",
    "https://kitomovies.me/home/"
]

# --- ROTATING AGENTS (To avoid blocking) ---
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
]

# --- COLORS ---
BLUE_BG = "\033[44;1;37m"
BLUE_TXT = "\033[1;34m"
GREEN_TXT = "\033[1;32m"
YELLOW_TXT = "\033[1;33m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear')

def get_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def make_clickable_link(url, text):
    # OSC 8 Escape Sequence for clickable terminal links
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def scrape_site(base_url, query):
    """Scrapes for Movies AND TV Shows."""
    search_url = f"{base_url}/search/{quote_plus(query)}"
    
    try:
        # Safety Delay
        time.sleep(DELAY) 
        response = requests.get(search_url, headers=get_headers(), timeout=6)
        
        if response.status_code != 200: return []

        soup = BeautifulSoup(response.text, 'html.parser')
        items = []

        # Matches class="flw-item" (Standard for these sites)
        for card in soup.select('div.flw-item'):
            try:
                link_tag = card.find('a')
                title = link_tag.get('title')
                href = link_tag.get('href')
                
                if href and not href.startswith('http'):
                    href = base_url + href
                
                # Metadata (Year / TV or Movie)
                meta = card.select('span.fdi-item')
                year = meta[0].text.strip() if len(meta) > 0 else "N/A"
                quality = meta[1].text.strip() if len(meta) > 1 else "TV/Movie"

                items.append({
                    'title': title,
                    'link': href,
                    'year': year,
                    'info': quality, # Shows if it is TV or Movie
                    'source': base_url.split('/')[2]
                })
            except: continue
        return items

    except Exception:
        return []

def main():
    # 1. UI SETUP
    clear_screen()
    print(BANNER) # <--- The Banner prints here!
    print(f" {BLUE_BG}  SEARCHING MOVIES & TV SHOWS  {RESET}\n")
    
    # Handle arguments or input
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input(f"{BLUE_TXT}⚡ Enter Title: {RESET}")
    
    if not query.strip(): sys.exit(1)

    # 2. SCANNING
    print(f"\n{YELLOW_TXT}Scanning sources (Agents Active)...{RESET}")
    all_results = []
    
    for url in URLS:
        # Print a blue dot for each site scanned
        print(f"{BLUE_TXT}•{RESET}", end="", flush=True) 
        results = scrape_site(url, query)
        all_results.extend(results)
    
    print("\n")

    if not all_results:
        print(f"{YELLOW_TXT}No results found.{RESET}")
        sys.exit(1)

    # 3. SELECTOR MENU
    clear_screen()
    print(BANNER)
    print(f"{BLUE_BG} FOUND {len(all_results)} RESULTS {RESET}\n")
    
    for idx, item in enumerate(all_results):
        # Display: 1) Title | 2024 | TV/Movie
        print(f"{BLUE_TXT}{idx + 1}){RESET} {item['title']} | {item['year']} | {item['info']}")

    try:
        choice = int(input(f"\n{BLUE_TXT}▶ Select Number: {RESET}")) - 1
        if choice < 0 or choice >= len(all_results): raise ValueError
        selected = all_results[choice]
    except:
        print("Invalid selection.")
        sys.exit(1)

    # 4. LAUNCHER SCREEN
    clear_screen()
    print(BANNER)
    print("\n")
    print(f"  {GREEN_TXT}✔  Ready: {selected['title']}{RESET}")
    print("  ==========================================")
    
    vlc_link = f"vlc://{selected['link']}"
    button_text = f"{BLUE_BG}  [ ▶ TAP TO OPEN IN VLC ]  {RESET}"
    
    print(f"\n      {make_clickable_link(vlc_link, button_text)}\n")
    print("  ==========================================")
    print("  Link expires in 15s...")
    time.sleep(15)
    clear_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")