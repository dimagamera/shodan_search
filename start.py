import shodan
import telebot
SHODAN_API_KEY = "PSKINdQe1GyxGgecYz2191H2JoS9qvgD"
api = shodan.Shodan(SHODAN_API_KEY)
bot = telebot.TeleBot("1161041702:AAH3kabwELLe_pRKuGZ51iyAAUtl8XtL9FU")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    bot.send_message(message.chat.id, "Starting...", reply_markup=keyboard)
    bot.send_message(message.chat.id, "[1] Пошук IP адресів")


@bot.message_handler(content_types=['text'])
def page_one(message):
    bot.send_message(message.chat.id, 'З якої сторінки?')
    bot.register_next_step_handler(message, page_two)


def page_two(message):
    global page_one
    page_one = message.text
    bot.send_message(message.chat.id, 'По яку сторінку? ')
    bot.register_next_step_handler(message, pages)


def pages(message):
    global page_two
    page_two = message.text
    bot.send_message(message.chat.id, "Напишіть запит")
    bot.register_next_step_handler(message, search)


def search(message):
    global search
    search = message.text
    if search == message.text:
        f = open('text.txt', 'w')
        for page in range(int(page_one), int(page_two)):
            results = api.search(message.text, page=page)
            for item in results['matches']:
                f.write(item['ip_str'] + "\n")
    f.close
    f = open("text.txt", 'rb')
    bot.send_document(message.chat.id, f)
    f.close


bot.polling(none_stop=True, interval=0)
