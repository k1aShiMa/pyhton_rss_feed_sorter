import feedparser
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import scrolledtext


#window
window = tk.Tk()
window.title("RSS Feed Viewer")
window.geometry("1280x720")

#text area where the text pops up
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
text_area.pack(expand=True, fill='both')

#rss_url = "https://feeds.feedburner.com/TheHackersNews"

feed = feedparser.parse("https://feeds.feedburner.com/TheHackersNews")

now =  datetime.utcnow()
last_24h = now - timedelta(hours=24)

# Print feed title
print(feed.feed.title)

# Loop through entries
for entry in feed.entries:
    if hasattr(entry, 'published_parsed'):
        entry_time = datetime(*entry.published_parsed[:6])
        if entry_time > last_24h:
            text_area.insert(tk.END, f"{entry.title}\n{entry.link}\n\n")

window.mainloop()