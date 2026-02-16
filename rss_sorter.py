import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime, timedelta
import feedparser
import re  # Added for searching CVE and CVSS patterns

# RSS Feed URL (NVD or specialized security feeds work best for this)
FEED_URL = "https://feeds.feedburner.com/TheHackersNews" 

def extract_security_info(text):
    """Searches text for CVE IDs and CVSS scores using regex."""
    # Pattern for CVE (e.g., CVE-2023-1234)
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    # Pattern for CVSS (looks for 'CVSS' followed by a number like 9.8 or 7.0)
    cvss_pattern = r'CVSS[:\s]*(\d{1,2}\.\d)'
    
    cves = re.findall(cve_pattern, text)
    cvss_match = re.search(cvss_pattern, text, re.IGNORECASE)
    
    found_cve = ", ".join(set(cves)) if cves else "None Found"
    found_cvss = cvss_match.group(1) if cvss_match else "N/A"
    
    return found_cve, found_cvss

# GUI Setup
window = tk.Tk()
window.title("Security RSS Feed Viewer")
window.geometry("1280x720")

# Input area for time and keywords
top_frame = tk.Frame(window)
top_frame.pack(pady=10)

time_input = tk.StringVar(value="24")
ttk.Label(top_frame, text="Hours:").grid(row=0, column=0, padx=5)
ttk.Entry(top_frame, textvariable=time_input, width=5).grid(row=0, column=1, padx=5)

keyword_input = tk.StringVar(value="fortinet, cisco, exploit")
ttk.Label(top_frame, text="Keywords:").grid(row=0, column=2, padx=5)
ttk.Entry(top_frame, textvariable=keyword_input, width=30).grid(row=0, column=3, padx=5)

# Text Display Area
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
text_area.pack(expand=True, fill='both', padx=10, pady=10)
text_area.configure(font=("Consolas", 11))
text_area.tag_config("title", foreground="blue", font=("Consolas", 12, "bold"))
text_area.tag_config("alert", foreground="red", font=("Consolas", 11, "bold"))

def fetch_feed():
    text_area.delete(1.0, tk.END)

    try:
        hours = int(time_input.get())
        cutoff = datetime.utcnow() - timedelta(hours=hours)
    except ValueError:
        text_area.insert(tk.END, "Error: Invalid hour count.\n")
        return

    keywords = [kw.strip().lower() for kw in keyword_input.get().split(",") if kw.strip()]
    feed = feedparser.parse(FEED_URL)
    
    if not feed.entries:
        text_area.insert(tk.END, "No entries found.\n")
        return

    for entry in feed.entries:
        # Check time
        if hasattr(entry, 'published_parsed'):
            entry_time = datetime(*entry.published_parsed[:6])
            if entry_time > cutoff:
                
                # Search title AND summary for keywords
                summary = entry.get('summary', '')
                content = (entry.title + " " + summary).lower()
                
                if not keywords or any(kw in content for kw in keywords):
                    # Extract CVE and CVSS
                    cve_id, cvss_score = extract_security_info(entry.title + " " + summary)
                    
                    # Formatting output
                    text_area.insert(tk.END, f"TITLE: {entry.title}\n", "title")
                    text_area.insert(tk.END, f"DATE:  {entry.published}\n")
                    text_area.insert(tk.END, f"CVE:   {cve_id}\n", "alert" if cve_id != "None Found" else "")
                    text_area.insert(tk.END, f"CVSS:  {cvss_score}\n", "alert" if cvss_score != "N/A" else "")
                    text_area.insert(tk.END, f"LINK:  {entry.link}\n")
                    text_area.insert(tk.END, "-"*80 + "\n\n")

ttk.Button(window, text="Fetch Security Feed", command=fetch_feed).pack(pady=5)

window.mainloop()
