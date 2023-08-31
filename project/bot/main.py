from telebot import TeleBot
from telebot.types import Message
import sqlite3
from time import sleep

bot = TeleBot('5483050351:AAEdp_yiQi3iWO_o5b4Cy_4KP8lfBZH85YU')

@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    print(chat_id)
    bot.send_message(chat_id, 'Hello')


def check_database():
    while True:
        sleep(10)
        database = sqlite3.connect('../db.sqlite3')
        cursor = database.cursor()

        cursor.execute('''
        SELECT text FROM fabrika_oldreport;
        ''')
        old_reports = cursor.fetchall()
        old_reports = [i[0] for i in old_reports]
        print(old_reports)
        cursor.execute('''
        SELECT text FROM fabrika_newreport;
        ''')
        new_reports = cursor.fetchall()
        new_reports = [i[0] for i in new_reports]
        print(new_reports)
        for i in old_reports:
            if i not in new_reports:
                bot.send_message('84779542', i)
                cursor.execute('''
                INSERT INTO fabrika_newreport(text) VALUES (?)
                ''', (i, ))
                database.commit()
        database.close()



if __name__ == '__main__':
    check_database()
