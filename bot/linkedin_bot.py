import time
import random
import urllib.parse
import os
import logging
import shutil
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LinkedInBot:
    """
    Automates LinkedIn connection requests with a focus on safety and human-like behavior.
    """
    
    def __init__(self, user_data_dir="chrome_data", state_file="bot_state.json"):
        self.driver = None
        self.user_data_dir = os.path.abspath(user_data_dir)
        self.is_running = False
        self.state_file = os.path.abspath(state_file)
        
        self._ensure_user_data_dir()

    def _ensure_user_data_dir(self):
        """Ensures the Chrome user data directory exists."""
        if not os.path.exists(self.user_data_dir):
            try:
                os.makedirs(self.user_data_dir)
            except Exception as e:
                logger.error(f"Failed to create user data dir: {e}")

    def _load_state(self):
        """Loads the bot state from a JSON file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load state: {e}")
        return {}

    def _save_state(self, state):
        """Saves the bot state to a JSON file safely."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=4)
        except PermissionError:
            logger.warning("Could not save state: Permission denied (file might be in use).")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def _setup_driver(self):
        """Initializes the Chrome WebDriver with persistent profile."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(f"user-data-dir={self.user_data_dir}")
        
        for attempt in range(3):
            try:
                service = Service(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            except SessionNotCreatedException:
                logger.warning(f"Session creation failed (Attempt {attempt+1}/3). Chrome might be already running.")
                if os.name == 'nt':
                    try:
                        os.system("taskkill /f /im chrome.exe")
                        time.sleep(2)
                    except:
                        pass
            except Exception as e:
                logger.error(f"Driver setup error: {e}")
                raise e
        
        raise WebDriverException("Failed to start Chrome after 3 attempts. Please close all Chrome windows.")

    def human_delay(self, min_seconds=2, max_seconds=5):
        """Sleeps for a random interval to mimic human interaction."""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def _generate_search_url(self, role, company, page=1, location="India"):
        """Constructs the search URL."""
        base_url = "https://www.linkedin.com/search/results/people/?"
        query_parts = [role]
        if company:
            query_parts.append(company)
        
        params = {
            "keywords": " ".join(query_parts),
            "origin": "GLOBAL_SEARCH_HEADER",
            "page": str(page)
        }
        
        if location.lower() == "india":
            params["geoUrn"] = '["102713980"]'
            
        return base_url + urllib.parse.urlencode(params)

    def start_automation(self, company, role, limit, callback=None):
        """Main execution method."""
        self.is_running = True
        
        def log(msg, type="info"):
            logger.info(msg)
            print(f"[{type.upper()}] {msg}")
            if callback:
                callback(msg, type)

        # State Management
        state_key = f"{company}_{role}"
        state = self._load_state()
        start_page = state.get(state_key, 1)

        try:
            log("Initializing browser...", "info")
            
            if self.driver:
                self.stop()
                
            self.driver = self._setup_driver()
            
            # Login Check
            log("Checking login status...", "info")
            self.driver.get("https://www.linkedin.com/feed/")
            self.human_delay(3, 5)
            
            if "feed" not in self.driver.current_url:
                log("Please log in manually in the browser window.", "warning")
                max_wait = 300 
                start_wait = time.time()
                while "feed" not in self.driver.current_url:
                    if not self.is_running: return
                    if time.time() - start_wait > max_wait:
                        log("Login timeout. Aborting.", "error")
                        return
                    time.sleep(2)
                log("Login detected. Proceeding...", "success")
            
            current_page = start_page
            if current_page > 1:
                log(f"Resuming search from page {current_page}...", "info")
            else:
                log(f"Starting new search: {role} at {company}", "info")

            # Search Execution
            search_url = self._generate_search_url(role, company, page=current_page)
            self.driver.get(search_url)
            self.human_delay(3, 5)
            
            total_sent = 0
            while total_sent < limit and self.is_running:
                # Find potential connection buttons
                xpath = "//button[.//span[text()='Connect'] or text()='Connect']"
                buttons = self.driver.find_elements(By.XPATH, xpath)
                
                log(f"Page {current_page}: Found {len(buttons)} potential connections.", "info")
                
                if not buttons:
                    log("No connectable profiles found on this page. Checking next page...", "warning")
                
                else:
                    for button in buttons:
                        if not self.is_running or total_sent >= limit:
                            break
                            
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                            self.human_delay(1, 2)
                            
                            if "Connect" not in button.text:
                                continue
                                
                            button.click()
                            self.human_delay(1, 2)
                            
                            # Handle "Send without note" Modal
                            try:
                                send_now = self.driver.find_element(By.XPATH, "//button[@aria-label='Send without a note']")
                                send_now.click()
                                total_sent += 1
                                log(f"Connection sent ({total_sent}/{limit})", "success")
                                self.human_delay(3, 6)
                            except:
                                # Fallback: Try generic "Send" button
                                try:
                                    send_btn = self.driver.find_element(By.XPATH, "//button[text()='Send']")
                                    send_btn.click()
                                    total_sent += 1
                                    log(f"Connection sent ({total_sent}/{limit})", "success")
                                    self.human_delay(3, 6)
                                except:
                                    log("Could not send request. Closing modal.", "warning")
                                    try:
                                        self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
                                    except: pass
                            
                            # Handle "Growing your network" Warning Popup
                            try:
                                got_it_btn = self.driver.find_elements(By.XPATH, "//button/span[text()='Got it']")
                                if got_it_btn:
                                    log("Dismissing 'Growing your network' popup...", "info")
                                    got_it_btn[0].click()
                                    self.human_delay(1, 2)
                            except:
                                pass
                                    
                        except Exception as e:
                            continue
                
                # Check for limit reached before paging
                if total_sent >= limit:
                    state[state_key] = current_page
                    self._save_state(state)
                    log(f"Limit reached. Progress saved at page {current_page}.", "info")
                    break
                    
                # Pagination
                try:
                    next_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                    if not next_btn.is_enabled():
                        log("Next button is disabled. No more pages.", "info")
                        break
                        
                    self.driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                    next_btn.click()
                    
                    # Update page count and save state
                    current_page += 1
                    state[state_key] = current_page
                    self._save_state(state)
                    
                    log(f"Navigating to page {current_page}...", "info")
                    self.human_delay(4, 6)
                except Exception as e:
                    log("No next page found or end of list.", "info")
                    break
            
            log(f"Task completed. Sent {total_sent} requests.", "success")
            log("BOT_FINISHED", "system") 
            
        except Exception as e:
            log(f"Error: {str(e)}", "error")
            log("Try clicking 'Stop' and restarting.", "warning")
            log("BOT_FINISHED", "system")
        finally:
            self.stop()

    def stop(self):
        """Stops the automation and closes the browser."""
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
