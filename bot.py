import os
import sqlite3
import humanize
import json
from datetime import datetime
from dotenv import load_dotenv
from pyrogram import Client, filters, enums
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

load_dotenv() 

# define constant parameters from env file
SERVER_NAME = os.environ.get('SERVER_NAME')
BOT_ID = os.environ.get('BOT_ID')
KEY1_TITLE = os.environ.get('KEY1_TITLE')
KEY1_URL = os.environ.get('KEY1_URL')
KEY2_TITLE = os.environ.get('KEY2_TITLE')
KEY2_URL = os.environ.get('KEY2_URL')
KEY3_TITLE = os.environ.get('KEY3_TITLE')
KEY3_URL = os.environ.get('KEY3_URL')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')
CHANNEL_ADDRESS = os.environ.get('CHANNEL_ADDRESS')

# instantiate a Client object from saved bot session
app = Client("myBot")

# convert En units to Fa units
def humanized_fa(my_str):
    output = humanize.naturalsize(my_str, binary=True)
    en_suffix = ["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    fa_suffix = ["کیلوبایت", "مگابایت", "گیگابایت", "ترابایت",
                 "پتابایت", "اگزابایت", "زبی‌بایت", "یوبی‌بایت"]
    for en, fa in zip(en_suffix, fa_suffix):
        output = output.replace(en, fa)
    return output

# query informantion about inbounds by port number
def get_inbound_info(user_uuid):
    try:
        count = 0
        sqliteConnection = sqlite3.connect('/etc/x-ui/x-ui.db')
        cursor = sqliteConnection.cursor()
        sql_select_query = "select * from inbounds"
        cursor.execute(sql_select_query)                       
        records = cursor.fetchall()
        if records:
            for row in records:
                user_uuidd = json.loads(records[count][11])['clients'][0]['id']
                if(user_uuidd == user_uuid):
                    uuser_port = row[9]
                    ser_status = True if row[6] == 1 else False
                    user_ul = humanized_fa(row[2])
                    user_dl = humanized_fa(row[3])
                    user_tot = humanized_fa(row[4])
                    user_used_vol = humanized_fa(row[3] + row[2])
                    user_used_pc = 100 * (row[2] + row[3]) / row[4]
                    expiry_date = datetime.fromtimestamp(row[7] // 1000)
                    current_date = datetime.today()
                    user_remark = row[5]
                count += 1
                
            result_query = (user_port, user_status, user_dl, user_ul, user_tot,
                            user_used_vol, user_used_pc, expiry_date, current_date, user_uuid, user_remark)
        else:
            result_query = None
        cursor.close()

        return result_query

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

# query informantion about expired inbounds
def get_expired_inbounds():
    try:
        sqliteConnection = sqlite3.connect('/etc/x-ui/x-ui.db')
        cursor = sqliteConnection.cursor()
        sql_select_query = """SELECT * from inbounds"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        current_date = datetime.today()
        expired_accounts = []
        if records:
            for row in records:
                user_used_pc = (row[2] + row[3]) / row[4]
                expiry_date = datetime.fromtimestamp(row[7] // 1000)
                if ((expiry_date - current_date).days <= 2) or (user_used_pc >= 0.9):
                    expired_accounts.append(
                        [row[9], row[5], expiry_date.strftime("%Y/%m/%d"),
                         humanize.naturalsize(row[3] + row[2], binary=True)])
            result_query = expired_accounts
        else:
            result_query = None
        cursor.close()

        return result_query

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


@app.on_message(filters.private & filters.command('start'))
async def send_welcome(client, message):
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(KEY1_TITLE, url=KEY1_URL),
             InlineKeyboardButton(KEY2_TITLE , url=KEY2_URL),],
            [InlineKeyboardButton(KEY3_TITLE , url=KEY3_URL), ],
        ],
    )

    info_text = f'سلام، به ربات تلگرامی {SERVER_NAME} خوش آمدید. با استفاده از کلیدهای زیر می‌توانید متناسب با سیستم عامل دستگاه خود، نرم‌افزار مربوطه را دانلود و نصب کنید. لطفاً جهت اطلاع از آخرین تغییرات و مطالب آموزشی در کانال تلگرامی ما عضو شوید.\n\n{CHANNEL_ADDRESS}'
    await app.send_message(message.chat.id,
                           info_text,
                           parse_mode=enums.ParseMode.HTML,
                           reply_markup=reply_markup,
                           disable_web_page_preview=True)


@app.on_message(filters.user(ADMIN_CHAT_ID) & filters.command('expired'))
async def send_expired(client, message):
    result_query = get_expired_inbounds()
    if result_query:
        info_text = ''
        for inbound in result_query:
            my_str = f'{inbound[0]} | {inbound[1]} | {inbound[2]} | {inbound[3]}\n'
            info_text += my_str
    else:
        info_text = 'هیچ حساب کاربری منقضی شده یا در آستانه انقضایی یافت نشد.'

    await app.send_message(message.chat.id,
                           info_text,
                           parse_mode=enums.ParseMode.HTML,
                           disable_web_page_preview=True)


@app.on_message(filters.text & filters.private)
async def send_information(client, message):
    request = message.text.split()
    if len(request) > 2 or request[0].lower() not in ["user",]:
        info_text = 'قالب دستور ارسال شده صحیح نمی‌باشد. لطفاً با قالب کلی <b>User 12345</b> ارسال کنید.'
    else:
        result_query = get_inbound_info(request[1])
        user_port, user_status, user_dl, user_ul, user_tot, user_used_vol, user_used_pc, expiry_date, current_date, user_uuid, user_remark = result_query
        if result_query and request[0].lower() == "user":
            info_text = f'تا ساعت {current_date.strftime("%H:%M")} تاریخ {current_date.strftime("%Y/%m/%d")}:\n\n<b>جزییات مصرف کاربر شماره {user_port}، بسته {user_tot}</b>\n\nحجم دانلود: {user_dl}\nحجم آپلود: {user_ul}\n\nکل حجم مصرف شده: {user_used_vol}\nدرصد مصرف شده: {user_used_pc:.1f} درصد\n\nحساب کاربری شما تا {(expiry_date - current_date).days} روز دیگر یعنی تا تاریخ {expiry_date.strftime("%Y/%m/%d")} اعتبار دارد. جهت تمدید سرویس می‌توانید از طریق ارتباط با پشتیبانی نسبت به شارژ مجدد حساب خود اقدام نمایید.'
        else:
            info_text = 'کاربری با مشخصات ارسالی پیدا نشد. لطفاً دوباره تست کنید.'

    await app.send_message(message.chat.id,
                           info_text,
                           parse_mode=enums.ParseMode.HTML,
                           disable_web_page_preview=True)


app.run()
