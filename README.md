🚨 Enterprise Security Advisory Pipeline
An automated intelligence pipeline designed to monitor global security advisories, filter them based on a specific company infrastructure stack, and deliver actionable alerts to Discord.

📖 Overview
This project solves the problem of "alert fatigue" by filtering out irrelevant security news and only notifying the team when a technology used in our environment is mentioned in a CVE or security advisory.

🛰️ Monitored Sources
The Hacker News (General Intelligence)

Fortinet Product Advisories (Network Security)

Cisco Security Center (Infrastructure)

CISA Cybersecurity Advisories (Government/Critical)

🛠️ Technology Stack
Python 3.11: Core logic, RSS parsing, and regex-based extraction.

Docker: Containerization for both the script and the n8n engine.

n8n: Workflow automation and message routing.

Discord: Final delivery platform for the alerts.

├── Dockerfile              # Container build instructions
├── requirements.txt        # Python dependencies (feedparser, requests)
├── rss_sorter.py           # Main logic & Filtering engine
└── README.md               # Documentation


🚀 Setup & Installation
1. n8n Configuration
Import or create a workflow with a Webhook Node.

Set the Method to POST and the Path to security-alert.

Connect it to a Discord Node using a Webhook URL.

2. Python Configuration
Open rss_sorter.py and modify the COMPANY_STACK list to include your technologies:

COMPANY_STACK = [
    "fortinet", "fortigate", "cisco", "ise", 
    "windows server", "exchange", "vmware", "esxi"
]

3. Build & Deployment
Build the image from the project root:
docker build -t security-sorter .

⚙️ Usage
Manual Run
To trigger an immediate scan:
docker run --rm --name security-scanner security-sorter

Automated Scheduling
To run the scan every morning at 08:00 AM, use a scheduler to start the container:

Windows (PowerShell):
# In Task Scheduler, set the action to:
docker start security-scanner

🔧 Networking Note (Docker Desktop)
If your n8n instance is running in a separate container on the same machine, ensure the N8N_WEBHOOK_URL in the Python script points to:
http://host.docker.internal:5678/webhook/security-alert

📊 Data Payload Example
The script sends the following JSON structure to n8n:
{
  "title": "Cisco ISE Remote Code Execution Vulnerability",
  "cve": ["CVE-2024-1234"],
  "cvss": "9.8",
  "urgency": "CRITICAL",
  "link": "https://tools.cisco.com/..."
}

🤝 Contribution
Update COMPANY_STACK as new hardware/software is onboarded.

Add new RSS sources to the FEEDS list.

Improve regex patterns for better CVSS extraction.

