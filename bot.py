from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram Bot Token from BotFather
TOKEN = "7714181082:AAE_yQaFDb4Wc17QXVFKUTVxCfb0J__2X60"

# Function to extract Mega link
def get_mega_link(ad_link):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(ad_link)
    time.sleep(5)  # Wait for redirection

    try:
        button = driver.find_element(By.XPATH, "//a[contains(text(), 'Get Link')]")
        button.click()
        time.sleep(3)
    except:
        return "Error: 'Get Link' button not found."

    final_link = driver.current_url
    driver.quit()
    return final_link

# Telegram command to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me an Adrinolinks link, and I'll get the direct Mega link for you!")

# Handle messages (extract links)
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    if "adrinolinks.in" in user_message:
        update.message.reply_text("Processing your request... Please wait.")
        direct_link = get_mega_link(user_message)
        update.message.reply_text(f"Here is your direct Mega link:\n{direct_link}")
    else:
        update.message.reply_text("Please send a valid Adrinolinks link.")

# Main function to run the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if _name_ == "_main_":
    main()
