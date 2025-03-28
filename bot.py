import logging
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Initialize Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token (Replace with your own Bot Token)
TOKEN = "7714181082:AAE_yQaFDb4Wc17QXVFKUTVxCfb0J__2X60"

# Function to Extract Mega Link
def get_mega_link(ad_link):
    # Chrome Options Setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Specify Chrome Binary Location
    chrome_bin = "/usr/bin/google-chrome-stable"  # Path on Render
    options.binary_location = chrome_bin

    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        logger.info("Opening the link...")
        driver.get(ad_link)
        time.sleep(5)  # Wait for initial page load

        # Wait for 'Get Link' button and click it
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Get Link')]")))
        button.click()
        logger.info("Button clicked. Waiting for redirection...")

        # Wait for URL to change
        initial_url = driver.current_url
        wait.until(lambda d: d.current_url != initial_url)
        final_link = driver.current_url

        logger.info(f"Final link found: {final_link}")
        driver.quit()
        return final_link

    except TimeoutException:
        logger.error("Timeout: Element not found or page took too long to load.")
        driver.quit()
        return "Error: Page took too long to load or element not found."

    except Exception as e:
        logger.error(f"Exception: {e}")
        driver.quit()
        return f"Error: {str(e)}"

# Telegram Command to Start the Bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me an Adrinolinks link, and I'll get the direct Mega link for you!")

# Handle Messages (Extract Links)
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    if "adrinolinks.in" in user_message:
        update.message.reply_text("Processing your request... Please wait.")
        direct_link = get_mega_link(user_message)
        update.message.reply_text(f"Here is your direct Mega link:\n{direct_link}")
    else:
        update.message.reply_text("Please send a valid Adrinolinks link.")

# Main Function to Run the Bot
def main():
    # Initialize the Telegram Bot
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start Polling
    updater.start_polling()
    updater.idle()

# Run the Bot
if __name__ == "__main__":
    main()
