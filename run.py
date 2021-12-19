#!/home/pupkin/projects/salaries/venv_salary/bin/python3
import telebot
import yaml
from mail import Mail
from hh_request import HhRequest


def check_input(message):  # получаем фамилию
    input_list = message.text.split(';')
    if len(input_list) in (2, 3) and input_list[1].isdigit():
        vacancy, region = input_list[0], input_list[1]
        try:
            request = HhRequest(vacancy, region)
            result = request.get_vac_dict
            text_for_mail = ''
            text_for_tg = ''
            for id in result.keys():
                value = '   |   '.join(result[id])
                text_for_mail = f'{text_for_mail}\n\n{value}'
                list_for_tg = [result[id][0], result[id][1], result[id][2], result[id][4]]
                job_for_tg = ' | '.join(list_for_tg)
                text_for_tg = f'{text_for_tg}\n\n{job_for_tg}'
            if len(input_list) == 3:
                if input_list[2].count('@') == 1:
                    mail = Mail('python', text_for_mail, input_list[2].strip())
                    mail.send_mail()
            if len(text_for_tg) > 4096:
                for x in range(0, len(text_for_tg), 4096):
                    bot.send_message(message.from_user.id, text_for_tg[x:x + 4096])
            else:
                bot.send_message(message.from_user.id, text_for_tg)
        except Exception as e:
            print(e)
    else:
        bot.send_message(message.from_user.id, 'Не пойдет.\n Подумай о своем поведении\n Напиши /start')


with open(r'config.yaml') as mail_config:
    config = yaml.load(mail_config, Loader=yaml.FullLoader)
tg_id = config.get('config').get('tg_key')
bot = telebot.TeleBot(tg_id)

@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Введи слова для поиска;регион; адрес_почты(необязательно)")
        bot.register_next_step_handler(message, check_input);  # следующий шаг – функция check_input,
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


bot.polling()
