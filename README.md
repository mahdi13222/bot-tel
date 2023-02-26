## ربات تلگرام v2ray
### روش اول
ابتدا به سرور خود لاگین نموده و دستور زیر را در ترمینال وارد نمایید:
```
bash <(curl -Ls https://raw.githubusercontent.com/sheli1366/v2ray_tg_bot/main/setup.sh)
```
سپس در همان محیط ترمینال با استفاده از یک ادیتور متنی مانند `vim` یا `nano` فایل `.env` را ویرایش نمایید.
```
sudo nano /home/python/.env
```
چنانچه به هر دلیلی نتوانستید از این ستاپ استفاده کنید کافیست کدهای قسمت روش دوم را به صورت دستی وارد کنید.

### روش دوم
اگر روش بالا برای شما کارساز نبود، دستورات زیر را خط به خط درون ترمینال لینوکس وارد کنید:
```
sudo apt update && sudo apt upgrade -y
sudo apt install unzip python3-venv -y
sudo mkdir /home/python
cd /home/python
sudo curl -L -o bot.zip https://github.com/sheli1366/v2ray_tg_bot/archive/refs/heads/main.zip
sudo unzip -j bot.zip -d /home/python
python3 -m venv venv
source "venv/bin/activate"
pip install pyrogram tgcrypto humanize python-dotenv
chmod +x run.sh
sudo cp runbot.service /lib/systemd/system/runbot.service
```
***
### توضیح متغیرهای محیطی
در این فایل باید متغیرهای ربات خود را تعریف نمایید.
1. متغیرهای `API_ID` و `API_HASH` را با استفاده از پلتفرم [API تلگرام](https://my.telegram.org/auth) برای ربات خود ایجاد نمایید.
2. به ربات [@BotFather](https://t.me/botfather) تلگرام مراجعه نموده و یک ربات برای خود بسازید. آیدی ربات را برای متغیر `BOT_ID` و مقدار توکن ربات را برای متغیر `BOT_TOKEN` وارد نمایید.
3. روبروی متغیر `SERVER_NAME` یک نام دلخواه برای سرور خود بنویسید.
4. این ربات دارای سه کلید حبابی است. به ترتیب می‌توانید عنوان کلید و آدرس URL آنها را درون متغیرهای `KEY1_TITLE` و `KEY1_URL`  و ... وارد نمایید.
5. یک نفر را به عنوان ادمین ربات معرفی کنید. برای این کار کافیست شناسه چت ادمین را درون متغیر `ADMIN_CHAT_ID` وارد کنید.شناسه چت یا Chat ID خود را می‌توانید با استفاده از ربات تلگرامی [@RawDataBot](https://t.me/RawDataBot) به دست آورید.
6. در پایان می‌توانید آدرس کانال تلگرام پشتیبانی را درون متغیر `CHANNEL_ADDRESS` وارد نمایید.
***
پس از تعریف متغیرهای فوق و ذخیره فایل، لازم است یک بار به سرور تلگرام درخواست دهیم تا مالکیت ربات ما را بررسی کند. برای این کار باید دستور زیر را وارد نمایید.
```
python bot_auth.py
```
پس از چند لحظه و ایجاد ارتباط بین ربات شما و سرور API تلگرام می‌توانید با زدن کلید `Ctrl+C` عملیات را متوقف کنید.
ربات شما آماده کار است. کافیست دستورات زیر را وارد نمایید تا پس از هر بار ریستارت شدن سرور، ربات شما نیز به عنوان یک سرویس همراه لینوکس بوت گردد.
```
sudo systemctl daemon-reload
sudo systemctl enable runbot.service
sudo systemctl start runbot.service
```
***
### شیوه استفاده
در حال حاضر دو دستور برای این ربات تعریف شده است.
1. با استفاده از فرمت دستوری زیر می‌توانید میزان مصرف کاربر با پورت شماره 12345 را مشاهده کنید
```
User 12345
```
2. دستور زیر هم مختص ادمین ربات هست و فهرستی از اکانت‌های منقضی شده (زمان یا حجم) یا اکانت‌های نزدیک به انقضاء را نشان می‌دهد.
```
/expired
```
