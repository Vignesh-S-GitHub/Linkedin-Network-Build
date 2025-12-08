from flask import Flask, render_template, request, jsonify, Response
from bot.linkedin_bot import LinkedInBot
import threading
import json
import time

app = Flask(__name__)
bot = LinkedInBot()
bot_thread = None
logs = []

def add_log(message, type="info"):
    """Adds a log message to the global list."""
    timestamp = time.strftime("%H:%M:%S")
    logs.append({"time": timestamp, "message": message, "type": type})
    # Keep only last 100 logs
    if len(logs) > 100:
        logs.pop(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_thread
    
    if bot.driver is not None:
        return jsonify({"status": "error", "message": "Bot is already running!"})

    data = request.json
    company = data.get('company')
    role = data.get('role')
    
    try:
        limit = int(data.get('limit', 10))
        if limit < 1 or limit > 50:
            return jsonify({"status": "error", "message": "Limit must be between 1 and 50."})
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid limit value."})
    
    # Clear previous logs
    logs.clear()
    add_log(f"Starting bot for {company} - {role} ({limit} limit)...", "info")

    def run():
        bot.start_automation(company, role, limit, callback=add_log)

    bot_thread = threading.Thread(target=run)
    bot_thread.start()
    
    return jsonify({"status": "success", "message": "Bot process started."})

@app.route('/stop', methods=['POST'])
def stop_bot():
    bot.stop()
    add_log("Bot stopped by user.", "warning")
    return jsonify({"status": "success", "message": "Bot stopped."})

@app.route('/reset', methods=['POST'])
def reset_bot():
    """Force reset: stops bot and kills chrome processes."""
    bot.stop()
    # Force kill chrome on windows
    if os.name == 'nt':
        try:
            os.system("taskkill /f /im chrome.exe")
        except:
            pass
    add_log("System forcefully reset.", "error")
    return jsonify({"status": "success", "message": "System reset."})

@app.route('/logs')
def get_logs():
    return jsonify(logs)

if __name__ == '__main__':
    # debug=False prevents the auto-reloader (watchdog) and is better for "normal" use.
    app.run(debug=False, port=5000)
