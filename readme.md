# ⚡ Hermes Video System v4.0

**Hermes** is a lightweight, terminal-based video aggregator designed specifically for **iSH (Alpine Linux) on iOS**. It "hunts" across multiple video sources, bypasses all web-based redirects and ads, and provides a clean UI to stream content directly to the **VLC for Mobile** app.

[Image of a terminal interface with a clickable hyperlink button]

## ✨ Features

* **Zero-Ad Experience**: By using `curl` and text-parsing, Hermes never executes JavaScript, meaning ads and pop-up redirects physically cannot trigger.
* **Multi-Source Hunting**: Aggregates results from your private family websites and public HD sources simultaneously.
* **Identity Rotation**: Automatically rotates User-Agents to prevent server-side bot detection.
* **Visual UI**: Features a blue-themed search interface and a blank-screen selection menu using `fzf`.
* **VLC Integration**: Handover is handled via the `vlc://` protocol for a seamless "Tap-to-Play" experience.
* **History Log**: Keep track of your last 20 watched videos for instant resuming.

---

## 📱 Installation (iSH / Alpine Linux)

To set up Hermes on your iPhone, open the **iSH** app and follow these steps:

### 1. Install Dependencies
```bash
apk update
apk add curl fzf coreutils

1. Install Git
First, install the Git package:

Bash
apk add git

2. Clone the Repository
Now, use the standard git clone command. Replace your-username and your-repo with your actual GitHub details:

Bash
git clone https://github.com/eldhoGI2/hermes.git

3. Move the Script to System Path
Once cloned, enter the folder and move the script so you can use the hermes command from anywhere:

Bash
cd hermes
# Assuming your file is named hermes.sh
mv hermes.sh /usr/local/bin/hermes
# Give it permission to run
chmod +x /usr/local/bin/hermes
🛠 Troubleshooting for iSH
Because iSH is a "limited" environment, you might run into two common issues:

A. The "SSL/HTTPS" Error
If Git complains about "SSL certificate" or "https" protocols, you need to install the CA certificates:

Bash
apk add ca-certificates
B. The "Command not found" Error
If you type hermes and nothing happens, check if /usr/local/bin is in your system's search path:

Bash
echo $PATH
If you don't see /usr/local/bin in that list, you can run the script by typing its full path: /usr/local/bin/hermes

Download Hermes
 Clone your repository or create the file manually:

# Create the command file

nano /usr/local/bin/hermes

3. Set Permissions
Bash
chmod +x /usr/local/bin/hermes

🚀 How to Use
Simply type hermes from anywhere in your terminal:

Search: Enter the title of a movie or TV show.

Hermes will display a blue search bar while it hunts.

Select: A clean, blank screen will appear with your results.

Use arrow keys to choose and hit Enter.

Play: Hermes returns to the main screen with a green button.

Tap the [ ▶ TAP TO OPEN VLC ] link to start streaming.

Advanced Commands
hermes -c : Open Continue mode to see your watch history.

hermes -h : Show the messenger's help guide.

hermes -clear : Wipe your search and watch history.

🛠 Configuration
To add your own private websites, edit the URLS variable at the top of the script:

📜 Disclaimer
Hermes is a scraper tool for personal use. It does not host any content but merely acts as a messenger between the terminal and public/private web directories.

---

### Instructions for you (Eldho):
1.  Save this text as `README.md` in your project folder.
2.  Commit it: `git add README.md && git commit -m "Added iPhone setup guide"`
3.  Push it: `git push origin main`

### Why this README works:
* **Dependency List:** It tells the user they need `coreutils` (for the `shuf` command) and `fzf` immediately.
* **Pathing:** It explains exactly where to put the file (`/usr/local/bin/hermes`) so the command works globally.
* **Visual Cues:** It uses Markdown formatting to make the search and selection steps easy to read on a small phone screen.



**Would you like me to help you write a "Setup Script" (`install.sh`) so that you can just run one command and it does all the installing for you?**


