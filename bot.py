from certifi import contents
from telegram import update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import os
from decouple import config

Token = config("TOKEN")
PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ["TOKEN"]
API_ENDPOINT = 'https://dog.ceo/api/breeds/image/random'

"""
    From python-telegram-bot docs about the Updater class

    This class, which employs the telegram.ext.Dispatcher, provides a frontend to telegram.Bot to the programmer, so they can focus on coding the bot. 
    
    Its purpose is to receive the updates from Telegram and to deliver them to said dispatcher.

    Using the add_handler function to the dispatcher, we basically add a new command.

    The line dp.add_handler(CommandHandler(‘bop’, bop)) simply defines a new command that will be triggered with /bop , and as a result, will trigger a function bop that we will soon implement.

    Next, we set a webhook that will listen on 0.0.0.0 with the specified port.

"""
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('bop', bop))

    updater.start_webhook(listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN)

    updater.bot.setWebhook('https://your-app-name.herokuapp.com/' + TOKEN)

    updater.idle()

"""We get the image URL from the API and sent it through our chatbot"""
def bop(update, context):
    url = get_image_url()
    chat_id = update.message.chat.id
    context.bot.send_photo(chat_id=chat_id, photo=url)

# 
def get_url():
    contents = requests.get(API_ENDPOINT).json()
    url = contents['message']
    return url

# To verify that the url we got from the API is within the file extensions we expect it to be.
def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''

    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url

if __name__ == '__main__':
    main()