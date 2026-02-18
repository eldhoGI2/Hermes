#!/usr/bin/env python3

#!/bin/sh

# --- CONFIGURATION ---
VERSION="1.0.0"
URLS=("https://hdtodayz.uk"  "https://wvv-fmovies.com/home/" "https://ww25.soap2day.day/soap2day-r26n8/" "https://kitomovies.me/home/")
DELAY=1.0 
HIST_FILE="$HOME/.hermes_history"
[ ! -f "$HIST_FILE" ] && touch "$HIST_FILE"

# Rotating Costumes
AGENTS="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0
Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36
"
RANDOM_AGENT=$(echo "$AGENTS" | shuf -n 1)

# --- SCRAPER ENGINE ---
scrape_source() {
    site="$1"
    query="$2"
    site_name=$(echo "$site" | cut -d'/' -f3)
    resp=$(curl -s -L -m 10 -A "$RANDOM_AGENT" "${site}/search/${query}")
    echo "$resp" | sed -n 's|.*<div class="flw-item">.*href="\([^"]*\)" title="\([^"]*\)">.*<span class="fdi-item">\([^<]*\)</span>.*<span class="fdi-item [^"]*">\([^<]*\)</span>.*|['"$site_name"'] \2\t\3\t\4\t'"$site"'\1|p'
}

main() {
    # 1. BLUE SEARCH BUTTON UI
    clear
    printf "\n"
    # Create a "Blue Button" look using background colors
    printf "  \033[44;1;37m  SEARCHING EVERYTHING...  \033[0m\n\n"
    
    if [ -z "$1" ]; then
        printf "\033[1;34m⚡ Hermes Query: \033[0m"
        read -r query
    else
        query="$*"
    fi
    [ -z "$query" ] && exit 1

    # 2. THE HUNT (Background)
    temp_results=$(mktemp)
    for url in $URLS; do
        scrape_source "$url" "$(echo "$query" | tr ' ' '+')" >> "$temp_results"
        sleep "$DELAY"
    done

    # 3. TRANSITION TO BLANK SCREEN
    if [ ! -s "$temp_results" ]; then
        echo "Nothing found."
        rm "$temp_results"
        exit 1
    fi

    # Clear screen for the "Blank ISH" display
    clear
    
    # 4. SELECTOR (Blue themed FZF)
    # This uses --color to make the menu match your blue theme
    selection=$(cat "$temp_results" | awk -F'\t' '{print NR") " $1 " | " $2 " | " $3}' | \
        fzf --reverse \
            --header="HERMES SELECTOR - Pick your Movie/Series" \
            --prompt="▶ " \
            --color="bg+:#000080,bg:#000000,hl:#0000ff,fg+:#ffffff,header:#0000ff,prompt:#0000ff")

    [ -z "$selection" ] && clear && rm "$temp_results" && exit 1

    # 5. DATA EXTRACTION
    idx=$(echo "$selection" | cut -d')' -f1)
    movie_info=$(cat "$temp_results" | sed -n "${idx}p")
    title=$(echo "$movie_info" | cut -f1)
    final_url=$(echo "$movie_info" | cut -f4)
    rm "$temp_results"

    # 6. RETURN TO MAIN ISH & SHOW BUTTON
    clear
    printf "\n\n"
    printf "  \033[1;32m✔  Found: $title\033[0m\n"
    printf "  ==========================================\n\n"
    
    # The Manual "Tap to Open" Button
    printf "  \033[1;33m  CLICK THE BUTTON BELOW TO OPEN VLC  \033[0m\n\n"
    printf "      \e]8;;vlc://$final_url\a\033[42;1;37m  [ ▶ TAP TO OPEN VLC ]  \033[0m\e]8;;\a\n\n"
    
    printf "  ==========================================\n"
    printf "  Hermes will reset in 20 seconds...\n"
    sleep 20
    clear
}

main "$@"