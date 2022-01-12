from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import os
import telegram_send

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ["TOKEN"]
API_ENDPOINT = 'https://dog.ceo/api/breeds/image/random'


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



"""We get the image URL from the API and sent it through our chatbot"""
def bop(update, context):
    url = get_image_url()
    chat_id = update.message.chat.id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    return context

def hello(update):
    chat_username = update.message.chatid
    telegram_send.send(messages=f"Hello {chat_username} How may I help you")

    




def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('hello', hello))

    updater.start_webhook(listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN)

    updater.bot.setWebhook('https://doogram.herokuapp.com/' + TOKEN)

    updater.idle()



if __name__ == '__main__':
    main()
    hello()