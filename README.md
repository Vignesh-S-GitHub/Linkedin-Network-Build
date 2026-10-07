<div align="center">

# LinkedIn Network Builder
### A local dashboard for managing connection-request workflows

**Flask · Selenium · local browser session · human-controlled limits**

</div>

A small local web app for organizing a focused networking workflow by company and role. It opens a Chrome session for you to sign in manually, then helps process connection actions under the limits you set.

> Use this project cautiously and follow LinkedIn’s current terms and platform limits. Keep requests modest, review each action, and stop if LinkedIn displays a restriction or warning. This tool is intended for local, personal experimentation; it is not an official LinkedIn product.

## What it includes

- A dark dashboard for setting a target company, role, and request limit
- A local Chrome session with manual sign-in
- Selenium-based browser interaction and persistent local session data
- A force-reset control for recovering a stuck local Chrome session

## Run locally

### Requirements

- Python and the dependencies listed in `requirements.txt`
- Google Chrome

### Setup

```bash
git clone https://github.com/Vignesh-S-GitHub/Linkedin-Network-Build.git
cd Linkedin-Network-Build
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000), choose a conservative request limit, and sign in manually when the Chrome window opens. Run only on your own computer; do not deploy it to a cloud host or CI runner.

## Project structure

- `app.py` — Flask server and dashboard routes
- `bot/` — Selenium workflow
- `templates/` — dashboard HTML
- `static/` — styles and browser-side behavior

---

<p align="center"><sub>Local workflow assistance with platform rules and user judgment kept in view.</sub></p>
