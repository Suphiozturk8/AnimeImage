
import anime_images_api, telebot, os
from telebot.types import *

api = anime_images_api.Anime_Images()

BOT_TOKEN = input("Please enter BOT_TOKEN: ")
bot = telebot.TeleBot(BOT_TOKEN)

if os.name == "posix":
    os.system("clear")
else:
    os.system("cls")

@bot.message_handler(commands = ["start"])
def Welcome(message:str):
    keyboard = InlineKeyboardMarkup(row_width = 3)
    buttons = [
        ("Hug", "sfw_hug"),
        ("Kiss", "sfw_kiss"),
        ("Slap", "sfw_slap"),
        ("Wink", "sfw_wink"),
        ("Pat", "sfw_pat"),
        ("Kill", "sfw_kill"),
        ("Cuddle", "sfw_cuddle"),
        ("Hentai ⚤", "nsfw_hentai"),
        ("Boobs ⚤", "nsfw_boobs")
    ]
    keyboard.add(*[InlineKeyboardButton(text, callback_data = data) for text, data in buttons])

    user = message.from_user
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    start_message = f"""
*Hello* {mention}

*Welcome to this bot that provides anime images.
Now, it's time to choose your preferred image category.
We will provide you with stunning visuals of your favorite anime characters.
Please specify your favorite image category, and let's find fantastic images for you!*
"""

    try:
        bot.reply_to(
            message,
            start_message,
            parse_mode = "markdown",
            reply_markup = keyboard)
    except Exception as e:
        print(e) 



def sendphoto(bot, chat_id, photo, category, message_id):
    try:
        keyboard = InlineKeyboardMarkup()
        bt = category.split("_")[-1]
        next_button = InlineKeyboardButton(
            text = f"🔀 {bt.capitalize()} 🔀",
            callback_data = category)
        keyboard.add(next_button)
        
        try:
            bot.edit_message_media(
                chat_id = chat_id,
                message_id = message_id,
                media = InputMediaPhoto(photo),
                reply_markup = keyboard)
        except:
            bot.send_photo(
                chat_id,
                photo,
                reply_markup = keyboard)
    except Exception as e:
        print(e)


@bot.callback_query_handler(
    func = lambda call: True)
def All(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    command_map = {
        "sfw_hug": "hug",
        "sfw_kiss": "kiss",
        "sfw_slap": "slap",
        "sfw_wink": "wink",
        "sfw_pat": "pat",
        "sfw_kill": "kill",
        "sfw_cuddle": "cuddle",
        "nsfw_hentai": "hentai",
        "nsfw_boobs": "boobs"
    }
    try:
        if call.data in command_map:
            result = api.get_nsfw(command_map[call.data]) if "nsfw_" in call.data else api.get_sfw(command_map[call.data])
            sendphoto(bot, chat_id, result, call.data, message_id)
    except Exception as e:
        print(e)

print("Bot runing...")
bot.infinity_polling()