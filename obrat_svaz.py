from telebot import TeleBot, types
from pyTelegramBotCAPTCHA import CaptchaManager, CaptchaOptions, CustomLanguage

bot = TeleBot("YOUR TOKEN")
digits = "123 456 789 0"
de_options = CaptchaOptions(max_user_reloads = 5, max_attempts = 5, only_digits = True)
de_options.generator = "math" 
de_options.custom_language = CustomLanguage(text = 'Итак, #USER!\nРешите пример выбрав ответ, у вас есть пять попыток ответа ✅, если цифры плохо видны перезагрузите этой 🔄 кнопкой!', try_again = '❗ОЙ❗ Пожалуйста, попробуйте еще раз!', your_code = 'Ввод: ', wrong_user = '❌ : Это не ваша задача!', too_short = '❌ : Нам жаль! Похоже ваш ответ слишком короткий!Попробуйте еще раз!') #Use my language
de_options.timeout = 90

captcha_manager = CaptchaManager(bot.get_me().id, default_options=de_options, code_length = 8)

# Test command handler
@bot.message_handler(commands=["start"])
def test_captcha(message):
    captcha_manager.send_new_captcha(bot, message.chat, message.from_user)


# Handler for correct solved CAPTCHAs
@captcha_manager.on_captcha_correct
def on_correct(captcha):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Рекламные предложения", callback_data='1')
    button2 = types.InlineKeyboardButton("Опубликовать на канале", callback_data='2')
    markup.add(button1, button2)
    bot.send_message(captcha.chat.id, "✅ : Поздравляем! Вы прошли тест! Что бы вы хотели нам предложить?", reply_markup=markup)
    captcha_manager.delete_captcha(bot, captcha)

# Handler for wrong solved CAPTCHAs
@captcha_manager.on_captcha_not_correct
def on_not_correct(captcha):
    bot.send_message(captcha.chat.id, f"❌ : Нам жаль, вы не прошли проверку!")
    captcha_manager.delete_captcha(bot, captcha)


# Handler for timed out CAPTCHAS
@captcha_manager.on_captcha_timeout
def on_timeout(captcha):
    bot.send_message(captcha.chat.id, f"❌ : Нам жаль, время вышло!")
    captcha_manager.delete_captcha(bot, captcha)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == '1':
        bot.send_message(chat_id=call.message.chat.id, text='Пожалуста введите свое предложение о рекламе. Не забудте оставить контактные данные😉:')
        bot.register_next_step_handler(call.message, commercial_offer_handler)
    elif call.data == '2':
        bot.send_message(chat_id=call.message.chat.id, text='Пожалуйста, напишите то что хотите опубликовать на канале. Не забудте оставить контактные данные, по желанию!:')
        bot.register_next_step_handler(call.message, content_proposal_handler)
    else:
        captcha_manager.update_captcha(bot, call)

def commercial_offer_handler(message):
    bot.forward_message(chat_id='CHAT_ID YOUR', from_chat_id=message.chat.id, message_id=message.message_id)

def content_proposal_handler(message):
    bot.forward_message(chat_id='CHAT_ID YOUR', from_chat_id=message.chat.id, message_id=message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)