# cookies.txt export instructions

This project includes a placeholder `cookies.txt` file for yt-dlp/YouTube authentication.

How to export cookies (Netscape `cookies.txt` format):

- Easiest: install a browser extension such as "Get cookies.txt" and export cookies for `youtube.com`.
- Alternative (Python): use a small script that reads browser cookies and writes Netscape format (requires third-party libs).

Place the exported `cookies.txt` file in the project root (next to `bot.py`) or set environment variables:

PowerShell (current session):
```
$env:YTDLP_COOKIES_FILE = "${PWD}\cookies.txt"
$env:YTDLP_COOKIES_FROM_BROWSER = "chrome"
```

Then run your usual yt-dlp command; example:
```
yt-dlp --cookies "%CD%\cookies.txt" <video-url>
```

Notes:
- I cannot access your local browser from this environment to export cookies automatically.
- If you want, I can add a small Python helper to attempt export using `browser_cookie3` — tell me and I'll add it.# Cookies Export and Usage

Place an exported `cookies.txt` (Netscape format) in this repository root to allow `yt-dlp` to access authenticated YouTube content.

How to export cookies:

- Option A: Browser extension
  - Install an extension such as "Get cookies.txt" and export cookies in Netscape format.
  - Save the exported file here as `cookies.txt`.

- Option B: Let `yt-dlp` read from your browser (no file needed)
  - Set environment variable `YTDLP_COOKIES_FROM_BROWSER` to your browser name (e.g. `chrome`, `firefox`).

Environment examples (PowerShell):

```powershell
$env:YTDLP_COOKIES_FILE = "${PWD}\cookies.txt"
$env:YTDLP_COOKIES_FROM_BROWSER = "chrome"
```

Security note:

- Do not commit sensitive cookies to public repositories. This file may contain authentication tokens.
# cookies.txt and browser auth

This repository contains a `cookies.txt` placeholder to allow yt-dlp to use YouTube cookies or browser authentication.

How to export cookies (you must run these locally — I cannot access your browser):

- Browser extension: install an extension like "Get cookies.txt" and export cookies in "Netscape" format to `cookies.txt` in this project folder.
- yt-dlp option: set environment variable `YTDLP_COOKIES_FROM_BROWSER` to your browser name (e.g. `chrome`, `firefox`) and yt-dlp will read cookies from your browser.

PowerShell examples (run locally):

```powershell
# Set the cookies file path for current session
$env:YTDLP_COOKIES_FILE = "${PWD}\cookies.txt"

# Or let yt-dlp read directly from browser
$env:YTDLP_COOKIES_FROM_BROWSER = "chrome"

# Example: download a YouTube video using browser cookies
yt-dlp --cookies-from-browser chrome https://www.youtube.com/watch?v=VIDEO_ID
```

Notes:
- I cannot export cookies from your browser in this environment. Please export the cookies file locally and place it at `cookies.txt`, or set `YTDLP_COOKIES_FROM_BROWSER`.
- After adding your exported `cookies.txt`, the repository already contains the placeholder file `cookies.txt`.
