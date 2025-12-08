# LinkedIn Automation (LA) 🚀

**A local, safe, and efficient tool to automate LinkedIn connection requests.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)

---

## ⚠️ EDUCATIONAL PURPOSE ONLY

**PLEASE READ CAREFULLY BEFORE USE:**

This software is developed strictly for **educational purposes** to demonstrate browser automation using Selenium and Python.

> [!CAUTION]
> **Use at your own risk.**
> Automating actions on LinkedIn violates their [User Agreement](https://www.linkedin.com/legal/user-agreement) and [Professional Community Policies](https://www.linkedin.com/legal/professional-community-policies).
>
> **Potential Risks Include:**
>
> - Temporary account restriction.
> - Permanent account ban.
> - Flagging of your IP address.

**The authors of this repository are not responsible for any consequences resulting from the use of this tool.** We strongly recommend:

- **Do NOT** send more than 20 requests per day.
- **Do NOT** run this on a server (AWS/Azure/GitHub Actions) - **Always run locally**.
- Monitor your account health regularly.

---

## Features

- **🛡️ Safe & Local**: Runs on your own machine using your own IP, reducing detection risk compared to cloud bots.
- **🧠 Smart Automation**:
  - Filters by **Company** and **Role**.
  - Automatically handles "Connect" buttons.
  - Dismisses "Send with note" modals (sends without note).
  - **Auto-Dismisses** "You are growing your network too fast" warnings.
- **💾 Persistent Login**: Log in once manually; the bot saves your session locally so you don't have to log in again.
- **🎨 Modern UI**: A clean, dark-mode Web Interface to control the bot easily.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/linkedin-automation.git
    cd linkedin-automation
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Start the Application**:

    ```bash
    python app.py
    ```

2. **Access the Dashboard**:
    Open your browser and navigate to: `http://localhost:5000`

3. **Configure & Run**:
    - Enter your target **Company** (e.g., `Google`) and **Role** (e.g., `Software Engineer`).
    - Set a safe **Limit** (Recommended: < 10 for testing).
    - Click **Start Automation**.

4. **First Run**:
    - A Chrome window will open.
    - **Log in to LinkedIn manually**.
    - The bot will detect your login and proceed automatically.

## Project Structure

```text
linkedin-automation/
├── app.py                 # Flask Web Server entry point
├── bot/                   # Core Automation Logic
│   ├── __init__.py
│   └── linkedin_bot.py    # Selenium Bot Class
├── static/                # Frontend Assets
│   ├── style.css          # Premium Dark Mode Styles
│   ├── script.js          # UI Logic
│   └── logo.png           # App Logo
├── templates/             # HTML Templates
│   └── index.html         # Dashboard UI
├── requirements.txt       # Python Dependencies
└── README.md              # Documentation
```

## Troubleshooting

- **"Chrome not reachable"**: If the bot gets stuck or you see this error, click the yellow **Force Reset** button in the UI. This will forcibly close all Chrome instances and reset the driver.
- **Login Loop**: If the bot keeps asking you to login, ensure you are not using an Incognito window and that the `chrome_data` folder is being created.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
