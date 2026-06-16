# verkada-device-monitor



\# Verkada Device Health Monitor



I built this project after going deep into Verkada's API documentation 

and wanting to understand how device management works at enterprise scale. 

The result is a Python-based monitoring tool that connects to Verkada's 

REST API and tracks the health of cameras and access control devices in real time.



\---



\## Why I Built This



I've been learning about physical security infrastructure and kept coming 

back to one question — how do you actually know when something breaks in 

a large camera deployment? This tool is my answer to that. It pulls live 

device data, flags what's offline, calculates a fleet health score, and 

logs everything so there's always an audit trail.



The security layer came from my cybersecurity background. Monitoring tool 

or not, any system making API calls should be watching its own responses 

for anomalies. So I added that too.



\---



\## What It Does



\- Pulls real time camera and door status from Verkada's REST API

\- Detects offline devices and tracks consecutive failure counts

\- Calculates a fleet health score across all devices

\- Fires alerts only after a configurable threshold — not on single blips

\- Displays a live terminal dashboard with a visual health bar

\- Logs offline events to a daily CSV for audit trail

\- Detects API anomalies and logs them with severity levels



\---



\## Security Event Detection



One thing I wanted to make sure of — the tool watches its own API 

responses for anything suspicious:



| Event | Trigger | Severity |

|-------|---------|----------|

| UNAUTHORIZED | 401 response | CRITICAL |

| FORBIDDEN | 403 response | HIGH |

| MASS\_OFFLINE | 50%+ devices offline simultaneously | HIGH |

| RATE\_LIMITED | 429 response | MEDIUM |

| API\_ERROR | 500+ server error | LOW |



A sudden mass offline event could mean a network outage — or something worse. 

Flagging it automatically felt important.



\---



\## Tech Stack



\- Python 3.8+

\- Verkada REST API

\- Requests, Pandas, Python-dotenv

\- JSON and CSV for logging



\---



\## Project Structure

verkada-device-monitor/



│



├── README.md



├── requirements.txt



├── .env                  ← API keys (never committed)



├── config.py             ← Credentials and settings



├── main.py               ← Entry point



├── monitor.py            ← Core health monitoring logic



├── alerts.py             ← Two-tier alert system



├── dashboard.py          ← Terminal dashboard



├── security.py           ← API anomaly detection



└── logs/



├── offline\_log.csv   ← Daily offline device log



└── security\_log.json ← Security event log



\---



\## Setup



```bash

git clone https://github.com/Sanjananuguri/verkada-device-monitor.git

cd verkada-device-monitor

pip install -r requirements.txt

```



Create a `.env` file:



VERKADA\_API\_KEY=your\_api\_key\_here



VERKADA\_ORG\_ID=your\_org\_id\_here



Run it:

```bash

python main.py

```



\---



\## About Me



I'm Sanjana Nuguri — a cybersecurity professional with an MS in  Cybersecurity from the University of North Texas. My background is in SOC analysis, incident 

response, and security tooling. This project sits at the intersection of that background and a genuine interest in how physical security infrastructure is managed 

at scale.



SC-200 | ISC2 CC   

\[LinkedIn](https://linkedin.com/in/sanjananuguri)

