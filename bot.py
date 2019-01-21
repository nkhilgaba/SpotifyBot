import spotify
import telebot
import time

#Add token here
TOKEN = ''


def bot_init():
    bot = telebot.TeleBot(token=TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user = message.from_user
        user_id = user.id
        bot.reply_to(
            message, 'Welcome to SpotifyBot! New tracks will be sent to you when added to the Spotify library.')
        while True:
            urls, tracks_id = spotify.fetch()
            if len(urls) > 0:
                for url in urls:
                    bot.send_message(user_id, url)
                spotify.add_to_tracklist(tracks_id)
            time.sleep(20)

    print('Starting SpotifyBot....\n')
    print('SpotifyBot Started!')
    bot.polling()


try:
    while True:
        bot_init()
except:
    time.sleep(20)
    bot_init()
