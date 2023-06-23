import logging
import time
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from googleapiclient.discovery import build

API_KEY = 'YoutubeAPIKey'
TELEGRAM_BOT_TOKEN = 'Token'
CHANNEL_ID = 'YoutubeChannelID'
SECRET_CODE = 'bibik'

logging.basicConfig(level=logging.INFO)

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_subscriber_count():
    request = youtube.channels().list(part='statistics', id=CHANNEL_ID)
    response = request.execute()
    return int(response['items'][0]['statistics']['subscriberCount'])

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    secret_code = update.message.text.split(' ')[1] if len(update.message.text.split(' ')) > 1 else None

    if chat_id < 0 or (secret_code and secret_code.lower() == SECRET_CODE.lower()):  # Check if it's a group chat or secret code is provided
        context.chat_data['chat_id'] = chat_id
        context.chat_data['interval'] = 900  # Set default interval to 900 seconds
        update.message.reply_text('Hello! I will notify you about changes in the number of subscribers to your YouTube channel.')
    else:
        update.message.reply_text('This command is intended for use in group chats or after entering the secret code.')

def set_interval(update: Update, context: CallbackContext):
    if len(context.args) == 1:
        try:
            interval = int(context.args[0])
            context.chat_data['interval'] = interval
            update.message.reply_text(f'The update interval has been set to {interval} seconds.')
        except ValueError:
            update.message.reply_text('Enter a valid interval value (an integer in seconds).')
    else:
        update.message.reply_text('Use the /set_interval command with a single argument (an integer in seconds).')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set_interval", set_interval, pass_args=True))

    updater.start_polling()

    prev_subscriber_count = get_subscriber_count()
    while True:
        interval = None
        for chat_data in dispatcher.chat_data.values():
            if 'interval' in chat_data:
                interval = chat_data['interval']
                break
        if interval is None:
            interval = 900  # Set default interval to 900 seconds

        logging.info(f'Interval: {interval} seconds')
        time.sleep(interval)
        current_subscriber_count = get_subscriber_count()
        logging.info(f'Prev: {prev_subscriber_count}, Current: {current_subscriber_count}')
        if current_subscriber_count != prev_subscriber_count:
            message = f'The number of subscribers has changed: {prev_subscriber_count} -> {current_subscriber_count}'
            for chat_data in dispatcher.chat_data.values():
                if 'chat_id' in chat_data:
                    updater.bot.send_message(chat_id=chat_data['chat_id'], text=message)
            prev_subscriber_count = current_subscriber_count

if __name__ == '__main__':
    main()
