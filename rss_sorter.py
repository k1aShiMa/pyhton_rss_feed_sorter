import feedparser
import re
import requests
import json
from datetime import datetime, timezone, timedelta

# --- Company STACK & config ---
# keywords for your company's stack and infra y'know like a whitelist
# AND ALSO you can modify this list, so if your environment isn't contains like nginx or something you can just delete that lol
COMPANY_STACK = [
    "fortinet", "fortios", "forticlient", "fortigate",
    "cisco", "ise", "catalyst", "rv340", 
    "windows server", "active directory", "exchange",
    "vmware", "esxi", "vcenter",
    "f5", "big-ip",
    "apache", "log4j", "nginx", "elastic",
    "kibana", "chrome", "signal", "redhat",
    "grafana", "slack", "atlassian",
    "bamboo", "jira", "moodle",
    "zabbix", "vscode", "notepad++",
    "docker", "trend micro", "wireshark",
    "men & mice", "men and mice", "n8n",
    ""
    ]

# blacklisted words
EXCLUDE_KEYWORDS = ["android", "iphone", "macos"]

# Minimum CVSS score lol
MIN_CVSS = 0.0

N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/JPJbTokeegroikd2"

# You can modify the FEEDS list, cuz why not
FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews", #thehackernews
    "https://www.bleepingcomputer.com/feed/", #bleepingcomputer
    "https://filestore.fortinet.com/fortiguard/rss/ir.xml", #fortinet psirt
    "https://sec.cloudapps.cisco.com/security/center/psirtrss20/CiscoSecurityAdvisory.xml", #Cisco
    "https://www.cisa.gov/cybersecurity-advisories/ics-advisories.xml", # CISA
    "https://wid.cert-bund.de/content/public/securityAdvisory/rss" #wid-cert-bund = german rss feed
    #"C:\path\to-the\rss-file" #rss feed from a file
]

def extract_security_info(text):
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    cvss_pattern = r'CVSS[:\s]*(\d{1,2}\.\d)'
    cves = list(set(re.findall(cve_pattern, text, re.IGNORECASE)))
    cvss_match = re.search(cvss_pattern, text, re.IGNORECASE)
    
    score = float(cvss_match.group(1)) if cvss_match else 0.0
    return (cves if cves else ["None Found"]), score

def is_relevant(title, summary):
    content = (title + " " + summary).lower()
    
    # 1. Checking if it's in the blacklist
    if any(ex in content for ex in EXCLUDE_KEYWORDS):
        return False
        
    # 2. Checking if it's in the whitelist
    if any(tech in content for tech in COMPANY_STACK):
        return True
        
    return False

def fetch_and_alert():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)
    print(f"[*] Starting targeted scan for company stack...")

    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if hasattr(entry, 'published_parsed'):
                entry_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if entry_time < cutoff:
                    continue

            summary = entry.get('summary', '')
            
            # --- Filtering logic ---
            if is_relevant(entry.title, summary):
                cve_ids, cvss_score = extract_security_info(entry.title + " " + summary)
                
                # Filtering for CVSS score
                if cvss_score < MIN_CVSS and cvss_score != 0.0:
                    continue

                payload = {
                    "alert_type": "MATCHED_STACK",
                    "title": entry.title,
                    "cve": cve_ids,
                    "cvss": cvss_score if cvss_score > 0 else "N/A",
                    "link": entry.link,
                    "urgency": "CRITICAL" if cvss_score >= 9.0 else "HIGH" if cvss_score >= 7.0 else "INFO"
                }

                try:
                    requests.post(N8N_WEBHOOK_URL, json=payload)
                    print(f"[+] Alert sent for: {entry.title}")
                except Exception as e:
                    print(f"[!] Error: {e}")

if __name__ == "__main__":
    fetch_and_alert()