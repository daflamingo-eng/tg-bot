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
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token (Use Environment Variable)
TOKEN = os.environ.get("TOKEN")

# Function to Extract Mega Link
async def get_mega_link(ad_link):
    # Chrome Options Setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Initialize WebDriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        logger.info("Opening the link...")
        driver.get(ad_link)
        time.sleep(5)

        # Wait for 'Get Link' button and click it
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Get Link')]")))
        button.click()
        logger.info("Button clicked. Waiting for redirection...")

        # Wait for URL to change
        initial_url = driver.current_url
        wait.until(lambda d: d.current_url != initial_url)
        final_link = driver.current_url

        logger.info(f"Final link found: {final_link}")
        return final_link

    except TimeoutException:
        logger.error("Timeout: Element not found or page took too long to load.")
        return "Error: Page took too long to load or element not found."

    except Exception as e:
        logger.error(f"Exception: {e}")
        return f"Error: {str(e)}"

    finally:
        driver.quit()

# Telegram Command to Start the Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an Adrinolinks link, and I'll get the direct Mega link for you!")

# Handle Messages (Extract Links)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if "adrinolinks.in" in user_message:
        await update.message.reply_text("Processing your request... Please wait.")
        direct_link = await get_mega_link(user_message)
        await update.message.reply_text(f"Here is your direct Mega link:\n{direct_link}")
    else:
        await update.message.reply_text("Please send a valid Adrinolinks link.")

# Main Function to Run the Bot
async def main():
    # Initialize the Telegram Bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start Polling
    await app.run_polling()

# Run the Bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
