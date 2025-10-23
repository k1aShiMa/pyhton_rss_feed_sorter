import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime, timedelta
import feedparser

#RSS Feed URL
FEED_URL = "https://feeds.feedburner.com/TheHackersNews"  # Replace with your feed

#GUI Setup
window = tk.Tk()
window.title("RSS Feed Viewer")
window.geometry("1280x720")


#time filter
time_input = tk.StringVar()
ttk.Label(window, text="Show entries from the last X hours:").pack(pady=5)
time_entry = ttk.Entry(window, textvariable=time_input)
time_entry.pack()
time_input.set("24")  # default value

#Text Display Area
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
text_area.pack(expand=True, fill='both', padx=10, pady=10)
text_area.configure(font=("Courier New", 11))
text_area.tag_config("title", foreground="blue", font=("Helvetica", 12, "bold"))

#Fetch Button Action
def fetch_feed():
    text_area.delete(1.0, tk.END)
    feed = feedparser.parse(FEED_URL)
    try:
        hours = int(time_input.get())
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=hours)
    except ValueError:
        text_area.insert(tk.END, "Please enter a valid number of hours.\n")
        return

    for entry in feed.entries:
        if hasattr(entry, 'published_parsed'):
            entry_time = datetime(*entry.published_parsed[:6])
            if entry_time > cutoff:
                text_area.insert(tk.END, f"Title: {entry.title}\n")
                text_area.insert(tk.END, f"Published: {entry.published}\n")
                text_area.insert(tk.END, f"Link: {entry.link}\n")
                text_area.insert(tk.END, "-"*60 + "\n\n")

#Fetch Button
ttk.Button(window, text="Fetch RSS", command=fetch_feed).pack(pady=5)

#Run App
window.mainloop()