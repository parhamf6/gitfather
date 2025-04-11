from telegram import Update , Bot
from telegram.ext import Application, CommandHandler, CallbackContext 
from functools import wraps
import logging
import datetime
import asyncio
# Load settings
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.config_loader import load_setting
setting = load_setting()
from src.core.git_actions import get_zen_quotes , commit_quote , get_repo
from src.data.db_manager import add_user

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


ALLOWED_USERS = setting["telegram"].get("allowed_users")

async def notify_user(msg):
    bot_instance = Bot('8045494347:AAEPoPEOfLs1fMghuh-RZfGvEDsDyzbLCL0')
    for user_id in ALLOWED_USERS:
        try:
            await bot_instance.send_message(chat_id=user_id, text=msg)
        except Exception as e:
            print(f"failed to send to {user_id} : {e}")

def restricted(func):
    @wraps(func)
    async def wrapped(update:Update, context:CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            print(f"Unauthorized access denied for {user_id}.")
            await update.message.reply_text("Sorry, you are not authorized to use this bot. sooo Fuck off")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

# Function to send a new quote
@restricted
async def send_quote(update: Update, context: CallbackContext) -> None:
    new_quote = get_zen_quotes() 
    quote_message = f"\"{new_quote['q']}\"\n— {new_quote['a']}"
    await update.message.reply_text(quote_message)

# Command to start the bot
@restricted
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    add_user(user.id , user.username)
    await update.message.reply_text("Hello! I am your Gitfather bot. Type /help to get all the commands")

# Command for help
@restricted
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Use /quote to get a random quote.")


@restricted
async def commit_q(update: Update, context: CallbackContext) -> None:
    loading_msgs = ["Processing.","finding the repo", "getting the quote", "formatting quote", "connecting to github","sending quote","update repo file","uploading repo","returning the details","it most come in few moment","A new commit made by the Dom gitfather to family archive"]
    progress_msg = await update.message.reply_text("Processing")
    async def send_final_commit():
        send_commit = commit_quote(get_repo())
        q = send_commit[0]
        t = send_commit[-1]
        await update.message.reply_text(f"{q['q']} \nby: {q['a']} \n\n {t}")
    for msg in loading_msgs:
        await progress_msg.edit_text(f"{msg}")
        await asyncio.sleep(2)
    await send_final_commit()

# Main function to run the bot
def main():
    # Create the Application instance
    application = Application.builder().token(setting['telegram']['token']).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("quote", send_quote))
    application.add_handler(CommandHandler("commitq", commit_q))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()






# @restricted
# async def commit_q(update: Update, context: CallbackContext) -> None:
#     send_commit = commit_quote(get_repo())
#     q = send_commit[0]
#     t = send_commit[-1]
#     loading_msgs = ["Processing.", "Processing..", "Processing...", "Processing...."]
#     progress_msg = await update.message.reply_text("Processing")
#     for msg in loading_msgs:
#         await progress_msg.edit_text(f"{msg}")
#         await asyncio.sleep(2)
#     await update.message.reply_text(f"{q['q']} \nby:{q['a']} \n\nAdded on : {t}")




