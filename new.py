import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8728002028:AAEj-O8uSGRH7AMWPhh925c8Yx4JV6ux0bY'  # Botunun tokenini buraya yaz!

bot = telebot.TeleBot(API_TOKEN)
balances = {}
admins = [7089656336]  # Kendi Telegram ID'ni buraya ekle!

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Grubum", url="https://t.me/elkaide1988"),
        InlineKeyboardButton("Sahip👤", url="https://t.me/kiraflexx")
    )
    bot.reply_to(message, '''🎲 EL KAIDE KUMAR BOTUNA HOSGELDINIZ!
Oynamak için /komutlar yaz
İyi şanslar 💸 kumar kötüdür 🤠''', reply_markup=markup)

@bot.message_handler(commands=['komutlar'])
def komutlar(message):
    text = '''🎰 Kumar Botu Komutları:

/start 🖱️: Oyunu başlatır 💸
/risk 💸: Paranızı katla veya kaybet
/borc 🤝: Bir kullanıcıya para atar
/zenginler 🏅: En zenginleri gösterir
/bakiye 💰: Toplam paranı gösterir
/sifirla 🧹: Kullanıcının bakiyesini sıfırlar (admin)
/gonder 🎁: Kullanıcıya para gönderir (admin)
/ceza ❌: Kullanıcıdan para eksiltir (admin)'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['bakiye'])
def bakiye(message):
    user_id = message.from_user.id
    bakiye = balances.get(user_id, 1000)
    bot.reply_to(message, f"💰 Bakiyen: {bakiye} TL")

@bot.message_handler(commands=['risk'])
def risk(message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Lütfen miktarı sayı olarak yaz: /risk <miktar>")
        return
    miktar = int(parts[1])
    balances.setdefault(user_id, 1000)
    if balances[user_id] < miktar:
        bot.reply_to(message, "Yetersiz bakiye!")
        return
    import random
    if random.choice([True, False]):
        balances[user_id] += miktar
        bot.reply_to(message, f"🎉 Kazandın! Yeni bakiyen: {balances[user_id]} TL")
    else:
        balances[user_id] -= miktar
        bot.reply_to(message, f"😢 Kaybettin! Yeni bakiyen: {balances[user_id]} TL")

@bot.message_handler(commands=['borc'])
def borc(message):
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        bot.reply_to(message, "Kullanım: /borc <kullanıcı_id> <miktar>")
        return
    to_id = int(parts[1])
    miktar = int(parts[2])
    balances.setdefault(to_id, 1000)
    balances[to_id] += miktar
    bot.reply_to(message, f"✅ {to_id} ID'li kullanıcıya {miktar} TL borç verdin.")

@bot.message_handler(commands=['zenginler'])
def zenginler(message):
    if not balances:
        bot.reply_to(message, "Henüz kimsenin bakiyesi yok.")
        return
    sirali = sorted(balances.items(), key=lambda x: x[1], reverse=True)[:10]
    text = "🏅 Zenginler Listesi:\n"
    for i, (uid, bakiye) in enumerate(sirali, 1):
        text += f"{i}. Kullanıcı {uid} - {bakiye} TL\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['sifirla'])
def sifirla(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "Bu komutu sadece adminler kullanabilir!")
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Kullanım: /sifirla <kullanıcı_id>")
        return
    to_id = int(parts[1])
    balances[to_id] = 0
    bot.reply_to(message, f"🔄 {to_id} ID'li kullanıcının bakiyesi sıfırlandı.")

@bot.message_handler(commands=['gonder'])
def gonder(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "Bu komutu sadece adminler kullanabilir!")
        return
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        bot.reply_to(message, "Kullanım: /gonder <kullanıcı_id> <miktar>")
        return
    to_id = int(parts[1])
    miktar = int(parts[2])
    balances.setdefault(to_id, 1000)
    balances[to_id] += miktar
    bot.reply_to(message, f"💸 {to_id} ID'li kullanıcıya {miktar} TL gönderildi.")@bot.message_handler(commands=['ceza'])
def ceza(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "Bu komutu sadece adminler kullanabilir!")
        return
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        bot.reply_to(message, "Kullanım: /ceza <kullanıcı_id> <miktar>")
        return
    to_id = int(parts[1])
    miktar = int(parts[2])
    balances.setdefault(to_id, 1000)
    balances[to_id] -= miktar
    bot.reply_to(message, f"🚫 {to_id} ID'li kullanıcının bakiyesinden {miktar} TL eksiltildi.")

bot.infinity_polling()
